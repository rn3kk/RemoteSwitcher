# R-140 RemoteSwitcher
Удаленное управление усилителем мощности Р-140 с блоком БМЗ

Этот проект разрабатывался в IDE JetBrains PyCharm Community Edition 2017.3.3
Он предназначен для управления усилителем мощности Р-140 с блоком механического запоминания (БМЗ). Предполагается что данный проект будет выполняться на миникомпьютерах серии Raspberry Pi или его аналогах.

Проект представляет собой веб сервер. Запустите проект. Октройте браузер. Наберите адрес http://127.0.0.1:81/ 
Браузер загрузит страницу управления усилителем мощности

<br>install python 2.7.9
<br>install pip
<br>install eventlet

У сервера есть авторизация, чтобы никто кроме Вас не мог переключить ничего в усилителе
![alt text](https://github.com/rn3kk/RemoteSwitcher/blob/master/img/autorise.PNG?raw=true)
В файле RemoteSwitcher/RemoteSwitcher/res/users можете добавлять пользователя
<br>RN3KK:passw
<br>RL3OH:passw2

Так выглядит окно управления. Помимо БМЗ можно включать удаленно трансивер или другие приборы
![alt text](https://github.com/rn3kk/RemoteSwitcher/blob/master/img/remswitcher.PNG?raw=true)

Из распберри берется код волны в бинармном виде и дешифратором в волну, которую необходимо включить.
![alt text](https://github.com/rn3kk/RemoteSwitcher/blob/master/img/deshifrator.png)

Ниже видео как сейчас это работает
[![IMAGE ALT TEXT HERE](https://github.com/rn3kk/RemoteSwitcher/blob/master/img/youtube.PNG)](https://youtu.be/m-rQdGDs2xI)


