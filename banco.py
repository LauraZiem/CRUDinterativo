# Alunos: Nicolas Edurado Jung Alves e Laura Ziem Teles França
# -*- coding: utf-8 -*-
from ast import Return
import sqlite3
import os
import sys
from time import sleep
from sqlite3 import Error
from xml.sax.handler import property_interning_dict


def conectarBanco():
    conexao = None
    try:
        database = 'banco.db'
        if not os.path.isfile(database):
            raise sqlite3.DatabaseError

        conexao = sqlite3.connect(f'file:{database}?mode=rw',
                                  uri=True)
    except sqlite3.DatabaseError:
        print('Erro: Banco de dados não existe')
        sys.exit()
    except Error as erro:
        print(erro)
        sys.exit()

    return conexao


def criarTabela(conexao):
    try:
        cursor = conexao.cursor()

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS funcionarios (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           nome TEXT, funcao TEXT, idade INTEGER
                       );
                       """)

        conexao.commit()
    except Error as erro:
        print(erro)
        sys.exit()
    finally:
        cursor.close()


def exibir_cabecalho(mensagem):
    mensagem = f'Rotina de {mensagem} de dados'

    print('\n' + '-' * len(mensagem))
    print(mensagem)
    print('-' * len(mensagem), '\n')

    id = input('ID (0 para voltar): ')

    return id


def mostra_registro(registro):
    print('\n===================')
    print('Registro')
    print('--------')
    print('ID:', registro[0])
    print('Nome:', registro[1])
    print('Função: ', registro[2])
    print('Idade: ', registro[3])
    print('===================')


def incluir(conexao):
    cursor = conexao.cursor()

    print("---------------------------")
    print("Rotina de inclusao de dados")
    print("---------------------------")
    nome = input('Nome (Deixe em branco para cancelar): ')
    if(nome == ""):
        return
    funcao = input('Função: ')
    idade = input('Idade: ')

    confirma = input('\nConfirma a inclusão [S/N]? ').upper()
    if confirma == 'S':
        comando = f'INSERT INTO funcionarios (nome, funcao, idade) VALUES("{nome}", "{funcao}", {idade})'
            # comando = f'INSERT INTO funcionarios(nome) VALUES("{nome}")'

        try:
            cursor.execute(comando)
        except Error as erro:
            print('Falha na inserção:', erro)
            sleep(5)
        else:
            conexao.commit()

    cursor.close()


def alterar(conexao):
    cursor = conexao.cursor()

    id = exibir_cabecalho('alteração')

    if int(id) == 0:
        return

    cursor.execute('SELECT * FROM funcionarios WHERE id=?', (id,))
    resultado = cursor.fetchone()

    if not resultado:
        print('\nID não existe!')
        sleep(2)
    else:
        mostra_registro(resultado)

        nome = input('\nNome: ')

        confirma = input('\nConfirma a alteração [S/N]? ').upper()
        if confirma == 'S':
            try:
                cursor.execute('UPDATE funcionarios SET nome=? WHERE id=?',
                               (nome, id))
            except Error as erro:
                print('Falha na alteração:', erro)
                sleep(5)
            else:
                conexao.commit()

    cursor.close()


def excluir(conexao):
    cursor = conexao.cursor()

    id = exibir_cabecalho('exclusão')

    if int(id) == 0:
        return

    cursor.execute('SELECT * FROM funcionarios WHERE id=?', (id,))
    resultado = cursor.fetchone()

    if not resultado:
        print('\nID não existe!')
        sleep(2)
    else:
        mostra_registro(resultado)

        confirma = input('\nConfirma a exclusão [S/N]? ').upper()
        if confirma == 'S':
            try:
                cursor.execute('DELETE FROM funcionarios WHERE id=?', (id, ))
            except Error as erro:
                print('Falha na exclusão:', erro)
                sleep(5)
            else:
                conexao.commit()

    cursor.close()


def listar(conexao):
    cursor = conexao.cursor()

    print('\n----------------------')
    print('Listagem dos Registros')
    print('----------------------\n')

    cursor.execute('SELECT * FROM funcionarios')
    registros = cursor.fetchall()

    for registro in registros:
        print('ID:', registro[0])
        print('Nome:', registro[1])
        print('Função: ', registro[2])
        print('Idade: ', registro[3])
        print('-----')

    print('\nPressione <ENTER> para continuar')
    sys.stdin.readline()


def menu(conexao):
    opcao = 1
    while opcao != 5:
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')

        print('--------------')
        print('MENU DE OPÇÕES')
        print('--------------')
        print('1. Incluir dados')
        print('2. Alterar dados')
        print('3. Excluir dados')
        print('4. Listar dados')
        print('5. Sair')
        opcao = int(input('\nOpção [1-5]: '))

        if opcao == 1:
            incluir(conexao)
        elif opcao == 2:
            alterar(conexao)
        elif opcao == 3:
            excluir(conexao)
        elif opcao == 4:
            listar(conexao)
        elif opcao == 5:
            print('\nEncerrando o programa...')
            sleep(2)

            if conn:
                conn.close()

            break
        else:
            print('Opção inválida, tente novamente')

        print()


if __name__ == '__main__':
    conn = conectarBanco()
    criarTabela(conn)
    menu(conn)
