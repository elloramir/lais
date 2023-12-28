# Requisitos
- HTML/CSS
- OOP
- Python/Django
- REST
- SQL/NOSQL?
- GIT/GH
- EDB
- Saúde digital

# O que é pra fazer
agendamendo online e triagem de candidatos a novos testes de COVID-19, com objetivo
de manter gestores atualizados em tempo real sobre o progresso da obtenção de candidatos.
o sistema deve permitir o autocadastro dos candidatos, validando informações como data de
nascimento, CPF e grupos de atendimento. Critérios para aptidão incluem não ter tido COVID
nos últimos 30 dias, ser maior de 18 anos e não pertencer a certos grupos específicos.
Além disso, há histórias de usuário para a página inicial, página de login, administração da
plataforma, listagem de exames, agendamento de exames e um painel administrativo.

# Páginas
- Página Inicial (História de Usuário #1):
Exibir informações do candidato autenticado (nome completo, data de nascimento, CPF,
aptidão para agendamento). Botão para encerrar sessão. Exibir botão para realizar agendamento, se apto.

- Autocadastro (História de Usuário #2):
Formulário para inserção de dados (nome completo, CPF, data de nascimento, grupos de atendimento,
se teve COVID nos últimos 30 dias, senha). Validação de dados (data de nascimento, grupos de atendimento,
CPF único). Critérios para aptidão na pesquisa.

- Página de Login (História de Usuário #3):
Formulário de login (CPF, senha). Mensagem de validação para CPF ou senha inválidos.
Redirecionamento para a página inicial após autenticação.

- Administração da Plataforma (História de Usuário #4):
Comando para inserir estabelecimentos de saúde.
Página de gerenciamento de estabelecimento (listagem com CNES e nome, filtro por CNES e nome).

- Listagem de Exames (História de Usuário #5):
Listagem de agendamentos para candidatos autenticados.
Informações sobre cada agendamento (data, hora, dia da semana, status, código e nome do estabelecimento).

- Agendamento de Exame (História de Usuário #6):
Formulário para agendamento (seleção de estabelecimento, horário, validação de horários e datas futuras).
Regras específicas para horários de agendamento.
Redirecionamento para a listagem de agendamentos após confirmação.

- Painel Administrativo (História de Usuário #7):
Exibição de gráficos (quantidade de agendamentos por estabelecimento, quantidade de usuários cadastrados aptos/inaptos).
Restrição de acesso para usuários não autenticados ou sem permissão de superusuário.