
# Como usar

## Dados de Entrada
Para os dados de entrada basta passa os arquivos input.txt e output.txt que se encontra na mesma altura do arquivo do teste.

## Executar o Código 

Para rodar os testes execulte esse comando no terminal apartir da pasta raiz.
```
python3 -m unittest test.test_balance

```

## Como instaciar a classe Balance
```
from Balance import Balance
balance = Balance('input.txt', 'output.txt')
balance.process()
```

## Resultado
Sera escrito o resultado no arquivo output.txt

## Observação
Se quiser testar novamente é bom apagar os dados do arquivo output.txt para ter a certeza de esta funcionando.


  