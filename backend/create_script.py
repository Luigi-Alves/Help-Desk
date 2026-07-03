# Este script é responsável por migrar os dados dos arquivos JSON para o banco de dados SQL.
# Ele deve ser executado apenas UMA VEZ, após a configuração inicial do banco de dados (Ele ja foi executado)
from app import app
from migrate import executar_migracao

if __name__ == '__main__':
    print('AVISO: Este script deve ser executado apenas UMA VEZ!')
    print('Ele migrará seus dados de JSON para SQL.')
    response = input('Deseja continuar? (s/n): ')
    
    if response.lower() == 's':
        executar_migracao(app)
        print('Migração concluída com sucesso!')
        print('Você pode agora deletar os arquivos JSON:')
        print('   - usuarios.json')
        print('   - chamados.json')
    else:
        print('Migração cancelada')