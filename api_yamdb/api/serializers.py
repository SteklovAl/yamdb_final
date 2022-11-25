from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from reviews.models import Categories, Comments, Genres, Review, Title

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализация данных категорий"""
    class Meta:
        fields = ('name', 'slug')
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    """Сериализация данных жанров"""
    class Meta:
        model = Genres
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    """Чтение информации о произведении"""
    category = CategorySerializer(read_only=True)
    genre = GenresSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    """Запись информации о произведении"""
    category = serializers.SlugRelatedField(
        slug_field='slug', many=False, queryset=Categories.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        required=False,
        queryset=Genres.objects.all()
    )
    lookup_field = 'id'

    class Meta:
        fields = '__all__'
        model = Title


class SignUpSerializer(serializers.Serializer):
    """Сериализация данных при регистрации."""
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )
    username = serializers.CharField(max_length=150, required=True)

    def validate(self, data):
        if data['username'].lower() == 'me':
            raise serializers.ValidationError('Нельзя использовать логин "me"')
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError(
                'Такой username уже зарегистрирован!'
            )
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                'Такой email уже зарегистрирован!'
            )
        return data

    class Meta:
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    """Сериализация данных при получении токена."""
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    """Сериализация данных пользователя."""
    email = serializers.EmailField(
        required=True,
    )
    username = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def validate_username(self, attrs):
        if User.objects.filter(username=attrs).exists():
            raise serializers.ValidationError(
                'Такой username уже зарегистрирован!'
            )
        return attrs

    def validate_email(self, attrs):
        if User.objects.filter(email=attrs).exists():
            raise serializers.ValidationError(
                'Такой email уже зарегистрирован!'
            )
        return attrs


class MeSerializer(serializers.ModelSerializer):
    """Сериализация данных своего профайла."""
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализация данных отзывов."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        title_id = (
            self.context['request'].parser_context['kwargs']['title_id']
        )
        title = get_object_or_404(Title, pk=title_id)
        user = self.context['request'].user
        if (
            self.context['request'].method == 'POST'
            and Review.objects.filter(author=user, title=title).exists()
        ):
            raise ParseError(
                'Можно оставить только один отзыв'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализация данных комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments
