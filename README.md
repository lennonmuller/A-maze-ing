# Grimorio do sabio (Dicionario):
##  Dataclassses: 
* dataclass: para inicializar uma classe de dados sem precisar de init.
* field: evita que instancias compartilhem listas/dicionarios (inicializacao controlada via formact_factory)
* IntEnum: Pode ser importada para comparacoes numericas
    * Herda o numero da variavel para calculos ou comparacoes
    * Permite operacoes bitwise(&, |, etc..)
        * Exemplo:  ``a.walls &= ~1``

## Orientacao das coordenadas
W = 8,
S = 4,
E = 2,
N = 1

* W S E N
* 8, 4, 2, 1

## Operacoes bitwise
* Bitwise AND (&): usado para verificar ou limpar bits
* Bitwise NOT (~): usado para inverter bits e abrir paredes
* bitmask -> Cada parede e um bit
    * ``self.walls &= ~wall``: abre a parede indicada
    * ``self.walls & wall``: verifica se a parede esta fechada

    ### exemplo
        1111 = todas as paredes fechadas = 15
            - abrit norte (0001) -> vira 1110 = 14
            - abrir south (0100) -> vira 1010 (-4) = 10


## decorador @property
#### Transforma o metodo em um atributo de somente leitura
* Permite que acesse um metodo como se fosse um atributo sem parenteses
    * Sem @property -> ``cell.hex_value()``
    * Com @property -> ``cell.hex_value``

* built-in, nao precisa importar
* impede atribuicao, vira somente leitura
