import flet as ft
import cryptocode as c

list_login = {
    'Lev Yamamoto': {'user': '56804', 'password': '27031998', 'id': 'assets/id_lev.png'},
    'Oscar Alho': {'user': '56806', 'password': '25122001', 'id': 'assets/id_oscar.png'},
    'Samuel Usher': {'user': '56805', 'password': '25081998', 'id': 'assets/id_samu.png'},
    'Gabriel Meireles': {'user': 'mei', 'password': 'mei', 'id': 'assets/id_bea.png'},
}

def main(page):
    page.title = "Ordo Realitas"

    def go_login(e): 
        page.views.pop() # remove pagina atual
        page.go("/") # vai para a pagina de login
    
    def go_dashboard(username):
        page.views.append(dashboard_page(username)) # adiciona dashboard a lista de paginas
        page.go("/dashboard")
        
    def go_id(user):
        page.views.append(id_page(user)) # adiciona dashboard a lista de paginas
        page.go("/id")

    def go_cod():
        page.views.append(cod_page()) # adiciona dashboard a lista de paginas
        page.go("/cod")

    def back_dashboard(e): 
        page.views.pop() # remove pagina atual
        page.go("/dashboard") # vai para a pagina de login
        
    def get_id(user):
        for name, data in list_login.items():
            if data ['user'] == user:
                return data['id']
            
    def get_name(user):
        for name, data in list_login.items():
            if data['user'] == user:
                return name
    
    def check_login(user, password):
        for name, data in list_login.items():
            if user == data["user"] and password == data["password"]:
                return name
        return None

    def login_page():
        def btn_click(e):
            user = txt_user.value
            password = txt_password.value
            
            if not user or not password:
                txt_user.error_text = "Não esqueça de fornecer o usuário"
                txt_password.error_text = "Não esqueça de fornecer a senha"
                page.update()
            else:
                username = check_login(user, password)
                if username:
                    txt_user.value = ""
                    txt_password.value = ""
                    go_dashboard(user)
                else:
                    txt_password.error_text = "Usuário ou senha incorretos"
                    txt_user.value = ""
                    txt_password.value = ""
                    page.update()
    
        txt_user = ft.TextField(hint_text="Usuário", color="white", width=400)
        txt_password = ft.TextField(hint_text="Senha", color="white", width=400, password=True)
        btn_connect = ft.OutlinedButton(
            text="Conectar",
            width = 400,
            height = 50,
            style = ft.ButtonStyle(
                color = "white",
                alignment=ft.alignment.center,  # Centraliza o texto no botão
            ),
            on_click=btn_click
        )

        return ft.View(
            "/",
            [
                ft.Container(
                    content=ft.Column(
                        [
                            txt_user,
                            txt_password,
                            btn_connect
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True,
                    ),
                    alignment=ft.alignment.center,
                    expand=True
                )
                    
            ],
            bgcolor= '#181818',
        )

    def dashboard_page(user):
        
        txt_welcome = ft.Text(
            value=f"Bem-vindo, agente {get_name(user)}!",
            size=20,
        )
        
        btn_id = ft.OutlinedButton(
            text="Identidade",
            width = 400,
            height = 60,
            style = ft.ButtonStyle(
                color = "white",
                alignment=ft.alignment.center,  # Centraliza o texto no botão
            ),
            on_click=lambda e: go_id(user)
        )

        btn_decod = ft.OutlinedButton(
            text="(Des)Criptografar",
            width = 400,
            height = 60,
            style = ft.ButtonStyle(
                color = "white",
                alignment=ft.alignment.center,  # Centraliza o texto no botão
            ),
            on_click=lambda e: go_cod()
        )

        btn_leave = ft.OutlinedButton(
            text="Sair",
            width = 400,
            height = 60,
            style = ft.ButtonStyle(
                color = "white",
                alignment=ft.alignment.center,  # Centraliza o texto no botão
            ),
            on_click=go_login
        )
        
        return ft.View(
            "/dashboard",
            [
                ft.Container(
                    content=ft.Column(
                        [
                            txt_welcome,
                            ft.Text(""),
                            btn_id,
                            btn_decod,
                            btn_leave,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True,
                    ),
                    alignment=ft.alignment.center,
                    expand=True
                )
            ],
            bgcolor= '#181818',
        )

    def id_page(user):

        identity = ft.Image(
            src = get_id(user),
            width = 400,
        )

        btn_back_dashboard = ft.OutlinedButton(
            text="Voltar",
            width = 400,
            height = 60,
            style = ft.ButtonStyle(
                color = "white",
                alignment=ft.alignment.center,  # Centraliza o texto no botão
            ),
            on_click=back_dashboard
        )
        
        return ft.View(
            "/id",
            [
                ft.Container(
                    content=ft.Column(
                        [
                            identity,
                            btn_back_dashboard,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True,
                    ),
                    alignment=ft.alignment.center,
                    expand=True
                )
            ],
            bgcolor= '#181818',
        )

    def cripto(key, msg, opt):
        if opt == "code":
            return c.encrypt(msg, key)
        else:
            return c.decrypt(msg, key)

    def cod_page():
        txt_key = ft.TextField(hint_text="Chave", color="white", width=400)
        txt_normal = ft.TextField(hint_text="Mensagem", color="white", width=400)
        txt_coded = ft.TextField(hint_text="Mensagem Codificada", color="white", width=400)

        txt_msg = ft.Text(value="", color="white")

        def btn_click(e):
            key = txt_key.value.strip() # strip() remove espaços iniciais e finais, caso sejam colocados
            normal = txt_normal.value.strip()
            coded = txt_coded.value.strip()

            if not key:
                txt_key.error_text = "É preciso informar a chave"
            else:
                if normal and not coded: # É porque precisa CODIFICAR
                    txt_msg.value = cripto(key, normal, "code")
                elif coded and not normal: # É porque precisa DECODIFICAR
                    txt_msg.value = cripto(key, coded, "decode")
                else:
                    txt_coded.error_text = "Preencha apenas um dos campos"

            page.update()
        
        btn_reveal = ft.OutlinedButton(
            text="Revelar",
            width=200,
            height=60,
            style=ft.ButtonStyle(
                color="white",
                alignment=ft.alignment.center,  # Centraliza o texto no botão
            ),
            on_click = btn_click
        )

        btn_back_dashboard = ft.OutlinedButton(
            text="Voltar",
            width=200,
            height=60,
            style=ft.ButtonStyle(
                color="white",
                alignment=ft.alignment.center,  # Centraliza o texto no botão
            ),
            on_click=go_login
        )

        return ft.View(
            "/cod",
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Column(
                                            [
                                                txt_key,
                                                txt_normal,
                                                txt_coded,
                                                btn_reveal
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            expand=True,
                                        ),
                                        alignment=ft.alignment.center,
                                        expand=True
                                    ),
                                    ft.Container(
                                        content=ft.Column(
                                            [
                                                txt_msg,
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            expand=True,
                                        ),
                                        alignment=ft.alignment.center,
                                        expand=True
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza o Row
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,  # Centraliza a Column
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True
                    ),
                    alignment=ft.alignment.center,  # Centraliza o Container inteiro
                    expand=True
                ),
                ft.Container(
                    content=btn_back_dashboard,
                    alignment=ft.alignment.bottom_right,
                    padding=30
                )
            ],
            bgcolor='#181818',
        )

    page.views.append(login_page())
    page.go("/")


ft.app(main)