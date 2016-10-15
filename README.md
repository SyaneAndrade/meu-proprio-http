# meu-proprio-http

Trabalho de Sistemas Distribuido
Curso Ciência da Computação
Universidade Federal de Uberlândia
Jessiane Gomes Andrade

Sistema de arquivo distribuido com servidor HTTPI

O objetivo deste projeto é desenvolver um sistema de arquivos
simplificado, gerenciado por um servidor HTTP e acessível por
clientes HTTP, seguindo a seguinte especificação:

>O Sistema de Arquivos (SA) é uma árvore.
>Cada nó do SA pode conter dados e ter filhos.
>Cada nó do SA é nomeado por uma string de no máximo 100
caracteres.
>O caminho completo, da raiz até o nó, pode ter qualquer
tamanho.
>Os dados de um nó são um vetor de no máximo 1KB.
>Não utilizar blibliotecas prontas para o HTTP


A linguagem utlizada é o python. O servidor foi implementado usando 
sockets.
Para maior esclarecimento quanto à ideia utilizei os seguintes tutoriais:

>Ruslan's Blog - Let’s Build A Web Server
>https://ruslanspivak.com/lsbaws-part1/

>Simple Python HTTP server using sockets
>http://blog.wachowicz.eu/?p=256

>SocketBasico
>http://wiki.python.org.br/SocketBasico

Para que o servidor se inicie, você pode executar o main.py. 
Para mudança de porta,
e o diretorio raiz é só editar o main.py.
Os teste estavam sendo feito utilizando o Postman.

Metodo GET do server

Recebe o path e verifica se é pra puxar da raiz ou de algum diretorio especifico,
procura nos diretorios iniciais no server e em seus nos, se achar retorna todos os
atributos e sua informações, se não retornar um Not Found.

Metodo POST do server

Recebe o path e verifica se tera que criar como raiz ou como no.
Quando achar seu respectivo lugar ele cria o novo no com a informação que foi inputada no
body da requisição, se não ele retorna um NOT FOUND, no caso do no já existir ele retorna como resposta
um BAD REQUEST.

Metodo PUT do server

Recebe o path para modificação da raiz ou do no. Verifica se o mesmo já existe.
Se existir ele modifica e retorna as informações já modificadas. Se não ele retorna um NOT FOUND.

Metodo DELETE do server

Receve o path para eliminar uma raiz ou um no. Verifica se o mesmo existe.
Se existir ele delete, se não retorna um NOT FOUND.


