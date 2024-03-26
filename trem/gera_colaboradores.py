import xlwt
from random import randint, choice

# Função para gerar um número de telefone fictício
def generate_phone_number():
    return f"({randint(10, 99)}) 9{randint(1000, 9999)}-{randint(1000, 9999)}"

# Dados dos funcionários
nomes_masculinos = ['Miguel', 'Arthur', 'Bernardo', 'Heitor', 'Davi', 'Lorenzo', 'Théo', 'Pedro', 'Gabriel', 'Enzo', 'Matheus', 'Lucas', 'Benjamin', 'Nicolas', 'Guilherme', 'Rafael', 'Joaquim', 'Samuel', 'Enzo Gabriel', 'João Miguel']
nomes_femininos = ['Alice', 'Sophia', 'Helena', 'Matilda', 'Manuela', 'Isabella', 'Heloísa', 'Luiza', 'Valentina', 'Maria Luiza', 'Júlia', 'Lorena', 'Lívia', 'Giovanna', 'Maria Eduarda', 'Beatriz', 'Mariana', 'Cecília', 'Eloá', 'Lara']

sobrenomes = ['Silva', 'Santos', 'Oliveira', 'Souza', 'Vidal', 'Costa', 'Ferreira', 'Rodrigues', 'Almeida', 'Carvalho', 'Gomes', 'Martins', 'Araújo', 'Lima', 'Lopes', 'Ribeiro', 'Alves', 'Monteiro', 'Barros', 'Nascimento']

departamentos = ['Marketing', 'Financeiro', 'Jurídico', 'Administrativo', 'TI']

def generate_email(nome):
    return f"{nome.lower().replace(' ', '_')}@alucario.com.br"

employees = []

for _ in range(50):
    nome = choice(nomes_masculinos + nomes_femininos)
    sobrenome = choice(sobrenomes)
    email = generate_email(f"{nome} {sobrenome}")
    departamento = choice(departamentos)
    telefone = generate_phone_number()
    # expiration_date = "31/12/2023"  # Data de expiração da senha fictícia
    employees.append((f"{nome} {sobrenome}", email, departamento, telefone))

# Criando o arquivo Excel
workbook = xlwt.Workbook()
sheet = workbook.add_sheet('Colaboladores')

# Escrevendo os cabeçalhos
headers = ['Nome', 'E-mail', 'Departamento', 'Telefone']
for col, header in enumerate(headers):
    sheet.write(0, col, header)

# Escrevendo os dados dos funcionários
for row, employee in enumerate(employees, start=1):
    name, email, department, phone_number = employee
    data = [name, email, department, phone_number]
    for col, value in enumerate(data):
        sheet.write(row, col, value)

# Salvando o arquivo
workbook.save('colaboradores.xls')
