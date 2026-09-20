import pytest
from main import BooksCollector


class TestBooksCollector:

    # 1. add_new_book — книга добавляется, жанр по умолчанию пустой
    def test_add_new_book_add_one_book(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        assert len(collector.get_books_genre()) == 1
        assert collector.get_books_genre()['Гарри Поттер'] == ''

    # 2. add_new_book — книги с названием длиннее 40 символов не добавляются
    # (параметризация: один сценарий, разные данные)
    @pytest.mark.parametrize('name', [
        'a' * 41,
        'a' * 100,
    ])
    def test_add_new_book_too_long_name_not_added(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert name not in collector.get_books_genre()

    # 3. add_new_book — одну и ту же книгу нельзя добавить дважды
    def test_add_new_book_duplicate_not_added_twice(self):
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.add_new_book('Дюна')
        assert len(collector.get_books_genre()) == 1

    # 4. set_book_genre + get_book_genre — жанр устанавливается,
    # только если он есть в списке допустимых жанров
    # (параметризация: один сценарий, разные жанры)
    @pytest.mark.parametrize('genre, expected', [
        ('Фантастика', 'Фантастика'),
        ('Ужасы', 'Ужасы'),
        ('Несуществующий жанр', ''),
    ])
    def test_set_book_genre(self, genre, expected):
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.set_book_genre('Дюна', genre)
        assert collector.get_book_genre('Дюна') == expected

    # 5. get_books_with_specific_genre — возвращает только книги нужного жанра
    def test_get_books_with_specific_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', 'Ужасы')
        collector.add_new_book('Дракула')
        collector.set_book_genre('Дракула', 'Ужасы')
        collector.add_new_book('Ну, погоди!')
        collector.set_book_genre('Ну, погоди!', 'Мультфильмы')

        result = collector.get_books_with_specific_genre('Ужасы')
        assert result == ['Оно', 'Дракула']

    # 6. get_books_genre — возвращает весь словарь книг с жанрами
    def test_get_books_genre_returns_full_dict(self):
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.set_book_genre('Дюна', 'Фантастика')
        assert collector.get_books_genre() == {'Дюна': 'Фантастика'}

    # 7. get_books_for_children — книги с возрастным рейтингом исключаются
    def test_get_books_for_children_excludes_age_rated_genres(self):
        collector = BooksCollector()
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', 'Ужасы')
        collector.add_new_book('Ну, погоди!')
        collector.set_book_genre('Ну, погоди!', 'Мультфильмы')

        result = collector.get_books_for_children()
        assert 'Оно' not in result
        assert 'Ну, погоди!' in result

    # 8. add_book_in_favorites — книгу можно добавить только если она есть
    # в словаре, и нельзя добавить повторно
    def test_add_book_in_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.add_book_in_favorites('Дюна')
        collector.add_book_in_favorites('Дюна')  # повторное добавление
        collector.add_book_in_favorites('Несуществующая книга')

        assert collector.get_list_of_favorites_books() == ['Дюна']

    # 9. delete_book_from_favorites — книга удаляется из избранного
    def test_delete_book_from_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.add_book_in_favorites('Дюна')
        collector.delete_book_from_favorites('Дюна')
        assert collector.get_list_of_favorites_books() == []

    # 10. get_list_of_favorites_books — возвращает список избранных книг
    def test_get_list_of_favorites_books(self):
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.add_new_book('Оно')
        collector.add_book_in_favorites('Дюна')
        collector.add_book_in_favorites('Оно')

        favorites = collector.get_list_of_favorites_books()
        assert favorites == ['Дюна', 'Оно']
        