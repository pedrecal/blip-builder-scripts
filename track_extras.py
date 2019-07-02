import sys
import json

EXTRAS = {
    'Nome': '{{contact.name}}',
    'Telefone': '{{contact.phoneNumber}}',
    'CPF': '{{contact.extras.cpf}}',
    'Id da Mensagem': '{{input.message@id}}',
    'Texto digitado': '{{input.content}}',
    'UserId': '{{contact.identity}}'
}


if len(sys.argv) < 2:
    print('uso: python tag_input.py <arquivo>')
    exit(-1)

arquivo_entrada = open(sys.argv[1], 'r')
fluxo = json.load(arquivo_entrada)
arquivo_entrada.close()

for bloco in fluxo:
    for acao in fluxo[bloco]['$enteringCustomActions'] + fluxo[bloco]['$leavingCustomActions']:
        if acao['type'] == 'TrackEvent':
            acao['settings']['extras'] = EXTRAS

nome_saida = '%s TRACKED.json' % (sys.argv[1].split('.')[0])
arquivo_saida = open(nome_saida, 'w')
arquivo_saida.write(json.dumps(fluxo))
arquivo_saida.close()

print('Feito! Salvo no arquivo %s' % nome_saida)
