import time

class Clock():
    '''
        FORMATO: Clock( pollTime )

        PARAMETROS:
            pollTime -> tiempo de ciclo en milisegundos
    '''
    def __init__(self,pollTime):
        self.TempsOld = round(time.time()*1000)
        self.TempsActual = round(time.time()*1000)
        self.TempsCicle = pollTime

    def timeout(self):
        '''
            FORMATO: timeout( )
                     El contador interno se resetea automàticamente.

            RETORNA:
                True    -> Final de Ciclo
                False   -> Esperando final de ciclo.
        '''
        self.TempsActual = round(time.time()*1000)
        if (self.TempsActual-self.TempsOld>= self.TempsCicle):
            self.TempsOld = self.TempsActual
            return True
        else:
            return False
    def restart(self):
        '''
            FORMATO: restart( )
                     Reinicia el contador interno.

            RETORNA:
                void
        '''
        self.TempsOld = round(time.time()*1000)

class TON():
    '''
        FORMATO: TON() - Temporizador con retardo a l'activación

        DIAGRAMA:
                 ___________
                |           |
            IN->|   TON()   |>-Q
            PT->|           |>-ET
                |___________|
    '''   
    def __init__(self):
        self._IN = False
        self._PT = 0
        self._Q = False
        self._ET = 0
        self.TempsOld = round(time.time()*1000)
        self.TempsActual = round(time.time()*1000)

    def update(self):
        '''
            FORMATO: update( )
                     Método para actualizar el contador interno y el estado de 
                     las variables.

            RETORNA:
                void
        '''       
        if self._IN:
            self.TempsActual = round(time.time()*1000)
            self._ET = self.TempsActual-self.TempsOld
            if (self._ET >= self._PT):
                self._Q=True
            else:
                self._Q=False
        else:
            self.TempsActual = round(time.time()*1000)
            self.TempsOld = self.TempsActual
            self._Q=False
        
    def IN(self,value):
        '''
            FORMATO: IN( valor )
                     Activacion del temporizador.

            PARAMETROS:
                value -> [True, False]

            RETORNA:
                void
        ''' 
        self._IN = value

    def PT(self,value):
        '''
            FORMATO: PT( value )
                     Cargar tiempo de contaje.
                     
            PARAMETROS:
                value -> [milisegundos]

            RETORNA:
                void
        '''        
        self._PT = value
    
    def Q(self):
        '''
            FORMATO: Q()
                     Final de contaje.

            PARAMETROS:
                NULL

            RETORNA:
                True    -> Temporizador Finalizado
                False   -> Esperando final de temporización.
        ''' 
        return self._Q
    
    def ET(self):
        '''
            FORMATO: ET()
                     Valor del contador interno.

            PARAMETROS:
                NULL

            RETORNA:
                TIME    -> Valor interno del Temporizador en milisegundos.
        ''' 
        return self._ET
    