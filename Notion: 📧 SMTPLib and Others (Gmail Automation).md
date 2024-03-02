# 📧 SMTPLib and Others (Gmail Automation)

# Teoria e prática do uso básico da SMTPLib.

A princípio, o uso básico do SMTP é bem simples, de forma teórica, é como preencher um e-mail, mas via código.

Segue o passo a passo do conceito abaixo:

1. Iniciamos a conexão do servidor da SMTPLib como se fossemos abrir o navegador, passando a porta de conexão ao servidor (Gmail).
2. Em seguida, passamos nossas credenciais, sendo o e-mail e a senha (a senha não é a mesma que você utiliza para entrar em sua conta Gmail).
3. Preenchemos o cabeçalho do e-mail, sendo o Título “Subject”, De “From” e Para “To”.
4. E finalizamos preenchendo nossa mensagem para depois enviar.
5. É uma boa prática fechar sua conexão de e-mail.

De forma resumida, este é o conceito teórico do seu uso.

Já para a explicação prática, iremos precisar da SMTPLib e também de outra biblioteca que tenha a função de “escrever” o corpo do e-mail, no exemplo da explicação foi utilizado a “email.message”.

1. Importamos as bibliotecas antes mencionadas e também utilizamos os parâmetros para configurar o servidor do SMTP conforme mostrado abaixo.

```python
import smtplib
from email.message import EmailMessage

# Configurações do servidor SMTP do Gmail
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'seu_email@gmail.com'
smtp_password = 'sua_senha'
```

2. Iniciamos a conexão e realizamos o login (como se fosse abrir o Gmail e realizar a autenticação).

```python
# Criar uma conexão segura com o servidor SMTP do Gmail
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(smtp_username, smtp_password)
```

3. Preenchemos os campos necessários do e-mail, sendo “Título“, “De“, “Para“ e o corpo do e-mail (desta vez utilizando o EmailMessage).

```python
# Criar o objeto de mensagem
msg = EmailMessage()
msg.set_content('Olá, esta é uma mensagem de teste!')
msg['Subject'] = 'Assunto do E-mail'
msg['From'] = smtp_username
msg['To'] = 'destinatario@email.com'
```

1. Para finalizar, enviamos o e-mail e fechamos conexão.

```python
# Enviar o e-mail
server.send_message(msg)

# Encerrar a conexão com o servidor SMTP
server.quit()
```

## Ideias para uso de envio de e-mails (conceito e prática).

**Conceito do dia a dia:**

No dia a dia, pode ser necessário enviar vários e-mails (neste caso, não serão abordados e-mails de resposta, mas a criação do assunto inicial) e até e-mails semelhantes, talvez mudando apenas os interessados que irão receber e um pouco do assunto, como datas, nomes, etc. De forma manual, é inteligente ter um padrão de e-mail para envio, com o corpo do e-mail padronizado onde ficarão destacados para alteração apenas os campos necessários (anteriormente mencionados). Na prática, copiamos, colamos e alteramos o campo, e assim continuamos até terminar todos os envios.

**Prática em código:**

Melhorando a ideia do nosso exemplo de código inicial, podemos e devemos construir uma classe para uso das funções básicas da SMTPLib, onde em nosso código que será realmente utilizado para o envio, passaremos as definições necessárias para uso.

```python
import smtplib
from email.message import EmailMessage

class ManagementEmail:
    def __init__(self) -> None:
        self.address = ""
        self.password = ""
        self.message = EmailMessage()
        self.smtp = None

    def authentication_files(self, address_file, password_file):
        with open(address_file) as file:
            self.address = file.read().strip()

        with open(password_file) as file:
            self.password = file.read().strip()

    def headers_email(self, title_email, recipient):
        self.message["Subject"] = title_email
        self.message["From"] = self.address
        self.message["To"] = recipient

    def message_email(self, message):
        self.message.set_content(message)

    def send_message(self):

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(self.address, self.password)
                smtp.send_message(self.message)
                print("Email sent successfully.")
        except Exception as e:
            print(f"Failed to send email. Error: {e}")
            
    def close_connection(self):
        if self.smtp:
            self.smtp.quit()
            print("SMTP connection closed.")
```

Acima está nosso código em classe, note como cada def em sequência segue a lógica do processo de enviar um e-mail. Abaixo, uma explicação rápida de cada def.

1. authentication_files, utilizado para localizar os txts contendo o e-mail e a senha para realizar o login.
2. headers_email, onde é iniciado o cabeçalho do e-mail.
3. message_email, criação do corpo do e-mail.
4. send_message, uso das defs anteriores criadas, note que "encapsulamos" as informações do e-mail dentro de "self.message".
5. close_connection, finalizamos a conexão com o servidor smtp.

Temos nossa classe contendo o uso básico da SMTPLib de forma organizada e lógica. Para realizar realmente uma automação de envios, basta apenas passar o seu arquivo JSON contendo suas chaves e valores, onde bastaria preencher os campos do cabeçalho e corpo de e-mail, caso queira enviar vários e-mails do mesmo endereço.

```json
[
    {
        "subject": "SMTPLib is awesome!",
        "destiny": "emailtesting@example.com",
        "content": "I can send mass and automatic emails using SMTP and Python"
    },
    {
        "subject": "SMTPLib is awesome!",
        "destiny": "emailtesting@example.com",
        "content": "I can send mass and automatic emails using SMTP and Python"
    }
]

```

Agora note que já temos toda a estrutura e mais os parâmetros preenchidos dentro do JSON. Neste momento, será necessário apenas criar o código que utilize esses itens para o envio em massa.

```python
import sys

sys.path.append("your/path/here")
from ClassSendEmail.management_email import *
import json

with open("address_for_send.json", "r") as file:
    data = json.load(file)

for information in data:
    email_management = ManagementEmail()

    email_management.authentication_files(
        address_file="address.txt", password_file="password.txt"
    )

    email_management.headers_email(title_email=information["subject"], recipient=information["destiny"])
    email_management.message_email(message=information["content"])
    email_management.send_message()

email_management.close_connection()

```

Acima está nosso código para uso dos envios automatizados. Abaixo uma explicação rápida do código.

1. Importamos as bibliotecas necessárias (note que não precisamos importar SMTP e EmailMessage, pois já estão presentes dentro da ClassSendEmail).
2. Passamos o caminho do nosso JSON e também o abrimos para leitura.
3. Iteramos data, sendo a variável que armazena as informações presentes no JSON, passando cada chave/valor para "information".
4. Iniciamos o uso de nossa classe, passando o para a variável "email_management".

*OBS: os próximos passos são literalmente idênticos aos mencionados na apresentação do uso básico da SMTP e EmailMessage.*

1. Passamos a localização dos txts contendo o e-mail e também a senha.
2. Preenchemos o cabeçalho do e-mail, note que usamos a variável "information", onde contém todos os valores presentes no JSON.
3. Preenchemos o corpo do e-mail "information["content"]".
4. E por fim, enviamos o primeiro e-mail contendo todas as informações do primeiro item dentro do JSON.
5. Após a iteração de todos os itens serem finalizados, fechamos a conexão com o servidor SMTP.

OBS: É inteligente fechar a conexão após o envio de todos os e-mails, evitando qualquer perda de envio durante a iteração e sobrecargas que podem gerar demoras ao enviar.

**Bônus: enviando anexo no e-mail:**

Para anexar arquivos no e-mail utilizando o SMTPLib é bem simples, sendo semelhante ao abrir o arquivo onde contém as credenciais para realizar a autenticação no Gmail.

```python
    def email_attachment(self, path_file, attachment_name):
        with open (path_file, "rb") as attachment:
            self.file_attachment = attachment.read()
            self.message.add_attachment(self.file_attachment, maintype="application", subtype="octet-stream", filename=attachment_name)
```

Acima está a nossa função criada dentro da classe. Abaixo, uma explicação rápida do código.

1. Devemos abrir o arquivo passando sua localização "path_file" no formato "rb" e definimos um apelido "as attachment".
2. Por ser uma def, definimos no início da classe o arquivo para leitura em "file_attachment".
3. Para finalizar, passamos a mensagem (EmailMessage) adicionando ao e-mail o anexo. Note todos os parâmetros que passamos, sendo o próprio anexo, o tipo de conteúdo, o subtipo e, para finalizar, o nome do anexo (como a pessoa que irá receber visualizará).

### Recapitulando o que aprendemos…

Como vimos, a SMTPLib juntamente com a EmailMessage são bibliotecas úteis e fáceis de se utilizar, tendo em mente o objetivo e a ideia de automação (mesmo que de forma conceitual), após aprender suas funções e lógica de implementação a mesma reduzirá um bom trabalho operacional do a dia administrativo.

Lembrando seu funcionamento, quase que literal, seguimos o mesmo passo a passo que faríamos se fossemos enviar um e-mail, sendo os abaixo.

1. Abrir o navegador (iniciar a conexão do SMTP).
2. Realizar o login (passar a localização das credenciais para leitura e utilizar no SMTP).
3. Preencher os cabeçalhos do e-mail (utilizamos o EmailMessage para isso).
4. Escrevemos nosso corpo de e-mail (passamos o conteúdo da messagem com EmailMessage).
5. Opcional: anexamos um arquivo para envio (utilizamos a função add_attachment do EmailMessage mais a lógica necessária para abertura e leitura do anexo).
6. Enviamos nosso e-mail já com tudo preenchido (utilizamos os parâmetros antes preenchidos para realizar envio).
7. Realizamos o logout e fechamos o navegador (finalizamos a conexão com o servidor SMTP).
