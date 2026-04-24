import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class MovieLibrary:
    def __init__(self, window):
        self.window = window
        self.window.title("Movie Library - Личная кинотека")
        self.window.geometry("1000x700")
        
        self.movies = []
        self.current_file = None
        
        self.setup_ui()
        self.create_table()
        
    def setup_ui(self):
        # Основной контейнер
        main_frame = ttk.Frame(self.window, padding=10)
        main_frame.pack(fill="both", expand=True)
        
        # Панель добавления фильма
        add_frame = ttk.LabelFrame(main_frame, text="Добавление фильма", padding=10)
        add_frame.pack(fill="x", pady=(0, 10))
        
        # Название
        ttk.Label(add_frame, text="Название:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.title_entry = ttk.Entry(add_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Жанр
        ttk.Label(add_frame, text="Жанр:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.genre_var = tk.StringVar()
        self.genre_combo = ttk.Combobox(add_frame, textvariable=self.genre_var, width=20)
        self.genre_combo['values'] = ('Боевик', 'Драма', 'Комедия', 'Фантастика', 
                                       'Ужасы', 'Триллер', 'Романтика', 'Документальный',
                                       'Анимация', 'Приключения', 'Криминал', 'Детектив')
        self.genre_combo.grid(row=0, column=3, padx=5, pady=5)
        self.genre_combo.set('Выберите жанр')
        
        # Год
        ttk.Label(add_frame, text="Год выпуска:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.year_entry = ttk.Entry(add_frame, width=10)
        self.year_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Рейтинг
        ttk.Label(add_frame, text="Рейтинг (0-10):").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.rating_entry = ttk.Entry(add_frame, width=10)
        self.rating_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Кнопка добавления
        ttk.Button(add_frame, text="Добавить фильм", command=self.add_movie).grid(row=1, column=4, padx=20, pady=5)
        
        # Панель фильтрации
        filter_frame = ttk.LabelFrame(main_frame, text="Фильтрация", padding=10)
        filter_frame.pack(fill="x", pady=(0, 10))
        
        # Фильтр по жанру
        ttk.Label(filter_frame, text="Жанр:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_genre = ttk.Combobox(filter_frame, width=20)
        self.filter_genre['values'] = ('Все', 'Боевик', 'Драма', 'Комедия', 'Фантастика', 
                                        'Ужасы', 'Триллер', 'Романтика', 'Документальный',
                                        'Анимация', 'Приключения', 'Криминал', 'Детектив')
        self.filter_genre.set('Все')
        self.filter_genre.grid(row=0, column=1, padx=5, pady=5)
        
        # Фильтр по году
        ttk.Label(filter_frame, text="Год выпуска:").grid(row=0, column=2, padx=5, pady=5)
        self.filter_year = ttk.Entry(filter_frame, width=10)
        self.filter_year.grid(row=0, column=3, padx=5, pady=5)
        
        # Кнопки фильтрации
        ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter).grid(row=0, column=5, padx=5, pady=5)
        
        # Панель статистики
        stats_frame = ttk.LabelFrame(main_frame, text="Статистика", padding=5)
        stats_frame.pack(fill="x", pady=(0, 10))
        
        self.stats_label = ttk.Label(stats_frame, text="Всего фильмов: 0 | Средний рейтинг: 0.00 | Лучший рейтинг: 0 | Худший рейтинг: 0", 
                                      font=('Arial', 9))
        self.stats_label.pack()
        
        # Панель кнопок файловых операций
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(file_frame, text="Сохранить в JSON", command=self.save_to_json).pack(side="left", padx=5)
        ttk.Button(file_frame, text="Загрузить из JSON", command=self.load_from_json).pack(side="left", padx=5)
        ttk.Button(file_frame, text="Очистить все фильмы", command=self.clear_all_movies).pack(side="left", padx=5)
        
        # Информационная панель
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill="x", pady=(0, 5))
        
        self.info_label = ttk.Label(info_frame, text="💡 Совет: Двойной клик по фильму для удаления", foreground="gray")
        self.info_label.pack()
        
    def create_table(self):
        # Таблица для отображения фильмов
        table_frame = ttk.Frame(self.window)
        table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        columns = ("#", "Название", "Жанр", "Год", "Рейтинг")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        self.tree.heading("#", text="#")
        self.tree.heading("Название", text="Название")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Год", text="Год")
        self.tree.heading("Рейтинг", text="Рейтинг")
        
        self.tree.column("#", width=50, anchor="center")
        self.tree.column("Название", width=300)
        self.tree.column("Жанр", width=150, anchor="center")
        self.tree.column("Год", width=80, anchor="center")
        self.tree.column("Рейтинг", width=100, anchor="center")
        
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        
        # Привязка двойного клика для удаления
        self.tree.bind("<Double-1>", self.delete_movie)
        
    def validate_year(self, year_str):
        try:
            year = int(year_str)
            if 1888 <= year <= 2025:  # Первый фильм появился в 1888 году
                return True, year
            return False, None
        except ValueError:
            return False, None
    
    def validate_rating(self, rating_str):
        try:
            rating = float(rating_str)
            if 0 <= rating <= 10:
                return True, rating
            return False, None
        except ValueError:
            return False, None
    
    def add_movie(self):
        title = self.title_entry.get().strip()
        genre = self.genre_var.get().strip()
        year_str = self.year_entry.get().strip()
        rating_str = self.rating_entry.get().strip()
        
        # Валидация
        if not title:
            messagebox.showerror("Ошибка", "Название фильма не может быть пустым")
            return
        
        if not genre or genre == 'Выберите жанр':
            messagebox.showerror("Ошибка", "Выберите жанр фильма")
            return
        
        valid_year, year = self.validate_year(year_str)
        if not valid_year:
            messagebox.showerror("Ошибка", "Год должен быть числом от 1888 до 2025")
            return
        
        valid_rating, rating = self.validate_rating(rating_str)
        if not valid_rating:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10")
            return
        
        movie = {
            "title": title,
            "genre": genre,
            "year": year,
            "rating": rating
        }
        
        self.movies.append(movie)
        self.refresh_table()
        self.update_statistics()
        
        # Очистка полей
        self.title_entry.delete(0, tk.END)
        self.genre_combo.set('Выберите жанр')
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)
        
        messagebox.showinfo("Успех", f"Фильм '{title}' добавлен в библиотеку")
    
    def refresh_table(self, filtered_movies=None):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        movies_to_show = filtered_movies if filtered_movies is not None else self.movies
        
        # Сортировка по году (от новых к старым)
        movies_to_show = sorted(movies_to_show, key=lambda x: x['year'], reverse=True)
        
        for i, movie in enumerate(movies_to_show, 1):
            self.tree.insert("", "end", values=(
                i,
                movie["title"],
                movie["genre"],
                movie["year"],
                f"{movie['rating']:.1f}"
            ))
    
    def update_statistics(self):
        if not self.movies:
            self.stats_label.config(text="Всего фильмов: 0 | Средний рейтинг: 0.00 | Лучший рейтинг: 0 | Худший рейтинг: 0")
            return
        
        total = len(self.movies)
        avg_rating = sum(m['rating'] for m in self.movies) / total
        max_rating = max(m['rating'] for m in self.movies)
        min_rating = min(m['rating'] for m in self.movies)
        
        self.stats_label.config(
            text=f"Всего фильмов: {total} | Средний рейтинг: {avg_rating:.2f} | "
                 f"Лучший рейтинг: {max_rating:.1f} | Худший рейтинг: {min_rating:.1f}"
        )
    
    def apply_filter(self):
        filter_genre = self.filter_genre.get()
        filter_year_str = self.filter_year.get().strip()
        
        filtered = self.movies.copy()
        
        # Фильтр по жанру
        if filter_genre and filter_genre != 'Все':
            filtered = [m for m in filtered if m["genre"] == filter_genre]
        
        # Фильтр по году
        if filter_year_str:
            valid_year, year = self.validate_year(filter_year_str)
            if not valid_year:
                messagebox.showerror("Ошибка", "Неверный формат года. Используйте число от 1888 до 2025")
                return
            filtered = [m for m in filtered if m["year"] == year]
        
        self.refresh_table(filtered)
        
        if filtered:
            avg_rating = sum(m['rating'] for m in filtered) / len(filtered)
            messagebox.showinfo("Фильтр", 
                               f"Найдено фильмов: {len(filtered)}\n"
                               f"Средний рейтинг: {avg_rating:.2f}")
        else:
            messagebox.showinfo("Фильтр", "Фильмов не найдено")
    
    def reset_filter(self):
        self.filter_genre.set('Все')
        self.filter_year.delete(0, tk.END)
        self.refresh_table()
    
    def delete_movie(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.tree.item(item, 'values')
        movie_title = values[1]
        
        if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить фильм '{movie_title}'?"):
            # Находим и удаляем фильм из списка
            for i, movie in enumerate(self.movies):
                if movie['title'] == movie_title:
                    self.movies.pop(i)
                    break
            
            self.refresh_table()
            self.update_statistics()
            messagebox.showinfo("Успех", f"Фильм '{movie_title}' удален")
    
    def clear_all_movies(self):
        if not self.movies:
            messagebox.showwarning("Предупреждение", "Нет фильмов для удаления")
            return
        
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить ВСЕ фильмы?\nЭто действие нельзя отменить!"):
            self.movies.clear()
            self.refresh_table()
            self.update_statistics()
            messagebox.showinfo("Успех", "Все фильмы удалены из библиотеки")
    
    def save_to_json(self):
        if not self.movies:
            messagebox.showwarning("Предупреждение", "Нет фильмов для сохранения")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Сохранить библиотеку фильмов"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.movies, f, ensure_ascii=False, indent=4)
                self.current_file = file_path
                messagebox.showinfo("Успех", f"Библиотека сохранена в {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")
    
    def load_from_json(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Загрузить библиотеку фильмов"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    loaded_movies = json.load(f)
                
                # Валидация загруженных данных
                for movie in loaded_movies:
                    if not all(k in movie for k in ("title", "genre", "year", "rating")):
                        raise ValueError("Неверный формат данных в файле")
                    if not (1888 <= movie["year"] <= 2025):
                        raise ValueError(f"Неверный год в фильме '{movie['title']}'")
                    if not (0 <= movie["rating"] <= 10):
                        raise ValueError(f"Неверный рейтинг в фильме '{movie['title']}'")
                
                self.movies = loaded_movies
                self.current_file = file_path
                self.refresh_table()
                self.update_statistics()
                self.reset_filter()
                messagebox.showinfo("Успех", f"Загружено {len(self.movies)} фильмов из {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")


if __name__ == "__main__":
    try:
        window = tk.Tk()
        app = MovieLibrary(window)
        window.mainloop()
    except ImportError:
        print("Ошибка: Tkinter не установлен.")
        print("На Linux установите: sudo apt-get install python3-tk")
        input("Нажмите Enter для выхода...")
