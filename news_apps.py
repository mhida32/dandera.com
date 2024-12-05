import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton,QLabel, QLineEdit,
    QTextEdit, QVBoxLayout, QHBoxLayoyt,QMessageBox, QScrollArea,
    QStackedWidget, QListWidget, QListWidgetItem, QFormLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class NewsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.auth = None # Данные для аунтефикации
        self.user_role = None # Роль пользователя
        self.current_news_id = None # Id текущей новости
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Новости приложения')
        self.resize(800,600)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;}
            QLabel {
                color: #333;
                font-size: 14px;}
            QPushButton:hover{
                background-color:#005f6d;}
            QPushButton {
                backgroud-color: #008CBA;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;}
            QLineEdit, QTextEdit {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;}
            QListWidget {
                background-color: white;
                border: 1px solid #ccc;}""")
        
    
    
    
    
    
    
    
    

        self.stacked_widget = QStackedWidget()
        
        #Создаем экраны виджетов
        self.login_widget = self.create_login_widget()
        self.register_widget = self.create_register_widget()
        self.main_menu_widget = self.create_main_menu_widget()
        self.news_list_widget = self.create_news_list_widget()
        self.news_detail_widget = self.create_news_detail_widget()
        self.create_news_widget = self.create_create_news_widget()
        
        #Добавляем экраны в QStackedWidget
        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.addWidget(self.register_widget)
        self.stacked_widget.addWidget(self.main_menu_widget)
        self.stacked_widget.addWidget(self.news_list_widget)
        self.stacked_widget.addWidget(self.news_detail_widget)
        self.stacked_widget.addWidget(self.create_news_widget)
        
        #Устанавливаем начальный экран
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)
        self.show_login_screen()
        
    #Создание экрана входа
    def create_login_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel("Вход в систему")
        title.setFont(QFont('Arial', 20))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        form_layout = QFormLayout()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Логин:", self.username_input)
        form_layout.addRow("Пароль:", self.password_input)
        layout.addLayout(form_layout)
        
        buttons_layout = QHBoxLayoyt()
        login_button = QPushButton("Войти")
        register_button = QPushButton("Регистрация")
        login_button.clicked.connect(self.login)
        register_button.clicked.connect(self.show_register_screen)
        buttons_layout.addWidget(login_button)
        buttons_layout.addWidget(register_button)
        layout.addLayout(buttons_layout)
        
        widget.setLayout(layout)
        return widget
    
    # Создание экрана регисрации
    def create_register_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel("Регистрация")
        title.setFont(QFont('Arial', 20))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        form_layout = QFormLayout()
        self.reg_username_input = QLineEdit()
        self.reg_password_input = QLineEdit()
        self.reg_password_input.setEchoMode(QLineEdit.Password)
        self.reg_role_input = QLineEdit()
        form_layout.addRow("Логин:", self.reg_username_input)
        form_layout.addRow("Пароль:", self.reg_password_input)
        form_layout.addRow("Роль (admin/editor/viewer):", self.reg_role_input)
        layout.addLayout(form_layout)
        
        buttons_layout = QHBoxLayoyt()
        register_button = QPushButton("Регистрация")
        back_button = QPushButton("Back")
        register_button.clicked.connect(self.register)
        back_button.clicked.connect(self.show_login_screen)
        buttons_layout.addWidget(register_button)
        buttons_layout.addWidget(back_button)
        layout.addLayout(buttons_layout)
        
        widget.setLayout(layout)
        return widget
    
    #Создание основного меню
    def create_main_menu_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.welcome_label = QLabel()
        self.welcome_label.setFont(QFont('Arial', 18))
        self.welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.welcome_label)
        
        buttons_layout = QFormLayout()
        view_news_button = QPushButton("Посмотреть новости")
        create_news_button = QPushButton("Создать новость")
        logout_button = QPushButton("Выйти")
        
        view_news_button.clicked.connect(self.show_news_list)
        create_news_button.clicked.connect(self.show_create_news_screen)
        logout_button.clicked.connect(self.show_logout)
        
        buttons_layout.addWidget(view_news_button)
        buttons_layout.addWidget(create_news_button)
        buttons_layout.addWidget(logout_button)
        layout.addLayout(buttons_layout)
        
        widget.setLayout(layout)
        return widget
    
    #Создание экрана списка новостей
    def create_news_list_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel("Новости")
        title.setFont(QFont('Arial', 18))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.news_list = QListWidget()
        layout.addLayout(self.news_list)
        
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.show_main_menu)
        layout.addLayout(back_button)
        
        widget.setLayout(layout)
        
        #Событие при клике на элемент списка
        self.news_list.itemClicked.connect(self.show_news_detail)
        
        return widget
    
    #Создание экран деталей новости
    def create_news_detail_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.news_detail_title = QLabel()
        self.news_detail_title.setFont(QFont('Arial', 18))
        layout.addWidget(self.news_detail_title)
        
        self.news_detail_author = QLabel()
        layout.addWidget(self.news_detail_author)
        
        self.news_detail_date = QLabel()
        layout.addWidget(self.news_detail_date)

        self.news_detail_content = QLabel()
        self.news_detail_content.setWordWrap(True)
        layout.addWidget(self.news_detail_content)

        buttons_layout = QHBoxLayoyt()
        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.show_new_list)
        buttons_layout.addWidget(back_button)
        self.delete_news_button = QPushButton("Удалить")
        self.delete_news_button.clicked.connect(self.delete_news)
        buttons_layout.addWidget(self.delete_news_button)
        layout.addLayout(buttons_layout)
        
        widget.setLayout(layout)
        return widget

    #Создание экрана создания новости
    def create_create_news_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        title_label = QLabel("Создать новость")
        title_label.setFont(QFont('Arial', 18))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        form_layout = QFormLayout()
        self.news_title_input = QLineEdit()
        self.news_content_input = QTextEdit()
        form_layout.addRow("Заголовок:", self.news_title_input)
        form_layout.addRow("Содержание:", self.news_content_input)
        layout.addLayout(form_layout)
        
        buttons_layout = QHBoxLayoyt()
        create_button = QPushButton("Создать")
        back_button = QPushButton("Назад")
        create_button.clicked.connect(self.create_news)
        back_button.clicked.connect(self.show_main_menu)
        buttons_layout.addWidget(create_button)
        buttons_layout.addWidget(back_button)
        layout.addLayout(buttons_layout)
        
        widget.setLayout(layout)
        return widget

    #Методы отображения экранов
    def show_login_screen(self):
        self.stacked_widget.setCurrentWidget(self.login_widget)

    def show_register_screen(self):
        self.stacked_widget.setCurrentWidget(self.register_widget)

    def show_main_menu(self):
        self.welcome_label.setText(f"Добро пожаловать,{self.username_input.text()}!")
        self.stacked_widget.setCurrentWidget(self.main_menu_widget)

    def show_news_list(self):
        self.news_list.clear()
        try:
            response = requests.get("http://localhost:8001/news/", auth=self.auth)
            if response.status_code == 200:
                self.news_data = response.json()
                for news in self.news_data:
                    item = QListWidgetItem(news['title'])
                    item.setData(Qt.UserRole, news)
                    self.news_list.addItem(item)
                self.stacked_widget.setCurrentWidget(self.news_list_widget)
            else:
                QMessageBox.warning(self,"Ошибка","Не удалось получить новости")
        except requests.exceptions.ConnectionError:
            QMessageBox.warning(self,"Ошибка","Не удалось подключиться к серверу API")

    def show_news_detail(self,item):
        news = item.data(Qt.UserRole)
        self.current_news_id = news['id']
        self.news_detail_title.setText(news['title'])
        self.news_detail_title.setText(f"Автор: {news['author_username']}")
        self.news_detail_author.setText(f"Дата: {news['created_at']}")
        self.news_detail_content.setText(news['content'])
        #Показываем кнопку удаления только для администратора 
        self.delete_news_button.setVisible(self.user_role == 'admin')
        self.stacked_widget.setCurrentWidget(self.news_detail_widget)

    def show_create_news_screen(self):
        if self.user_role not in ['editor','admin']:
            QMessageBox.warning(self,"Ошибка","У вас нет прав для создавания новостей")
            return
        self.news_title_input.clear()
        self.news_content_input.clear()
        self.stacked_widget.setCurrentWidget(self.create_news_widget)

    #Методы действий
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if not username or not password:
            QMessageBox.warning(self,"Ошибка","Пожалуйста, ввидите имя пользователя и пароль")
            return
        try:
            response = requests.post("http://localhost:8001/login/", auth=(username, password))
            if response.status_code == 200:
                self.auth = (username, password)
                self.user_role = response.json().get('role')
                QMessageBox.information(self,"Успех","Вы успешно вошли")
                self.show_main_menu()
            else:
                QMessageBox.warning(self,"Ошибка","Неверно имя пользователя или пароль")
        except requests.exceptions.ConnectionError:
                QMessageBox.warning(self,"Ошибка","Не удалось подключиться к серверу API")

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.reg_role_input.text() or 'viewer'
    
        #Проверка на заполненность полей
        if not username or not password:
            QMessageBox.warning(self,"Ошибка","Пожалуйста, заполните все поля")
            return

        # Формируем данные для регистрации
        data = {
            "username":username,
            "password":password,
            "role_name":role,
        }

        try:
            #Отправляем POST-запрос на сервер для регистрации
            response = requests.post("http://localhost:8001/register/", json=data)
            #Обработка ответа от сервера
            if response.status_code == 200:
                QMessageBox.information(self,"Успех","Регистрация прошла успешно")
                self.show_login_screen()
            elif response.status_code == 400:
                #Получаем подробное сообщение об ошибке
                detail = response.json().get("detail","Ошибка регисрации")
                if isinstance(detail,list):
                    detail = '\n'.join([str(item) for item in detail])
                elif isinstance(detail,dict):
                    detail = str(detail)
                QMessageBox.information(self,"Ошибка",detail)
                
            else:
                #Общая обработка для других структур
                QMessageBox.information(self,"Ошибка",f"Ошибка регистрации: {response.status_code}")
        except requests.exceptions.ConnectionError:
            QMessageBox.warning(self,"Ошибка","Не удалось подключиться к серверу API")
        except requests.exceptions.RequestException as e:
            QMessageBox.information(self,"Ошибка",f"Произошла ошибка: {str(e)}")

    

    def logout(self):
        self.auth = None
        self.user_role = None
        self.username_input.clear()
        self.password_input.clear()
        self.show_login_screen()

    def create_news(self):
        title = self.news_title_input.text()
        content = self.news_content_input.toPlainText()
        if not title or not content:
            QMessageBox.warning(self,"Ошибка","Пожалуйста, заполните все поля")
            return
        data ={
            "title":title,
            "content":content,
        }
        try:
            response = requests.post("http://localhost:8001/news/",auth=self.auth, json=data)
            if response.status_code == 200:
                QMessageBox.information(self,"Успех","Новость успешно создана")
                self.show_main_menu()
            else:
                detail = response.json().get("detail","Ошибка при создании новости")
                QMessageBox.warning(self,"Ошибка",detail)
        except requests.exceptions.ConnectionError:
            QMessageBox.warning(self,"Ошибка","Не удалось подключиться к серверу API")

    def delete_news(self):
        try:
            response = requests.post("http://localhost:8001/news/{self.current_news_id}",auth=self.auth)
            if response.status_code == 200:
                    QMessageBox.information(self,"Успех","Новость успешно удалена")
                    self.show_news_list()
            else:
                detail = response.json().get("detail","Ошибка при удалении новости")
                QMessageBox.warning(self,"Ошибка",detail)
        except requests.exceptions.ConnectionError:
                QMessageBox.warning(self,"Ошибка","Не удалось подключиться к серверу API")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    news_app = NewsApp()
    news_app.show()
    sys.exit(app.exec_())