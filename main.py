
class CycleCoding():

    correctSymbols = ('0', '1', '2', '3', '4',\
                    '5', '6', '7', '8', '9',\
                    '+', 'x', 'X')


    def take_degree(self,basis_of_degree):
        if basis_of_degree == '1':
            return 0
        if basis_of_degree == 'X':
            return 1
        return int(basis_of_degree[1:])


    def checkPxGx(self,expression, mode='Gx'):
        if mode == "Px":
            if not(expression.endswith('+1')):
                print('#!# Px не оканчивается на +1 #!#')
                return False

        for symbol in expression:
            if not (symbol in self.correctSymbols):
                print('#!# Выражение содержит недопустимые символы #!#')
                return False

        return True


    def biggest_degree(self,expression):
        biggest_degree_Px = 0
        for symbol in range(len(expression)):
            if biggest_degree_Px < self.take_degree(expression[symbol]):
                biggest_degree_Px = self.take_degree(expression[symbol])
        return biggest_degree_Px


    # If takes lists only!
    def mult_expression_on_biggerst_degree(self,multipliable, multiplier):
        if multiplier == ['X0']:
            return multipliable

        product = []
        biggest_degree_Px = self.biggest_degree(multiplier)

        for element in range(len(multipliable)):
            if multipliable[element] == '1':
                product.append('X' + str(biggest_degree_Px))
                continue
            if multipliable[element] == 'X':
                product.append('X' + str(biggest_degree_Px + 1))
                continue
            product.append('X' + str(int(multipliable[element][1:]) + biggest_degree_Px))
        return product


    def GxXn_div_Px(self,GxXn, Px):
        Cx = []
        Rx = ['X999']
        Px_Set = set(Px)
        GxXn_Set = set(GxXn)
        count = 1
        while self.biggest_degree(Rx) >= self.biggest_degree(Px):
            if count == 5:
                pass
            # print('')
            # print(GxXn)
            Rx_Set = set(self.mult_expression_on_biggerst_degree(Px, ['X' + str(self.biggest_degree(GxXn) - self.biggest_degree(Px))]))
            # print(Rx_Set)
            if ('X' + str(self.biggest_degree(GxXn) - self.biggest_degree(Px))) == 'X0':
                Cx.append('1')
            else: Cx.append('X' + str(self.biggest_degree(GxXn) - self.biggest_degree(Px)))
            Rx_Set = GxXn_Set^Rx_Set

            Rx = list(Rx_Set)
            GxXn = list(Rx_Set)
            GxXn_Set = set(GxXn)

            count += 1

        return [Rx, Cx]


    def GxXnRx_div_Cx(self,GxXn, Rx, Cx):
        GxXn_Rx = list(set(GxXn)|set(Rx))
        Px = []
        Rx = ['X999']
        Cx_Set = set(Cx)
        GxXn_Rx_Set = set(GxXn_Rx)

        while self.biggest_degree(Rx) >= self.biggest_degree(Cx):
            # print('')
            # print(Rx)
            Rx_Set = set(self.mult_expression_on_biggerst_degree(Cx, ['X' + str(self.biggest_degree(GxXn_Rx) - self.biggest_degree(Cx))]))
            # print(Rx_Set)
            if ('X' + str(self.biggest_degree(GxXn_Rx) - self.biggest_degree(Cx))) == 'X0':
                Px.append('1')
            else: Px.append('X' + str(self.biggest_degree(GxXn_Rx) - self.biggest_degree(Cx)))
            Rx_Set = GxXn_Rx_Set^Rx_Set

            Rx = list(Rx_Set)
            GxXn_Rx = list(Rx_Set)
            GxXn_Rx_Set = set(GxXn_Rx)

        if Rx == []:
            Rx = 0

        return [Rx, Px]


    def get_Gx_impulses(self,Gx, GxXn):
        impuls = []
        for element in range(int(Gx[0][1:]), 0, -1):
            # print(element)
            if ('X' + str(element)) in Gx:
                impuls.append(1)
            else:
                impuls.append(0)

        if '1' in Gx:
            impuls.append(1)
        else:
            impuls.append(0)

        for i in range(int(GxXn[0][1:]) - int(Gx[0][1:])):
            impuls.append(0)

        # print(impuls)

        return impuls


    def get_Px_coder(self,Px):
        coder = []
        for element in range(1, int(Px[0][1:])):
            # print(element)
            if ('X' + str(element)) in Px:
                coder.append('XOR')
                coder.append('X' + str(element))
            else:
                coder.append('X' + str(element))

        if ('1' in Px):
            coder.insert(0, '1')
            coder.insert(0, 'XOR')
        else:
            coder.insert(0, 'X1')

        return coder


    def show_coder(self,coder):
        print('-----Coder------')
        for i in range(len(coder)):
            print(i, coder[i])

        return coder



    def XOR(self,a, b):
        if a == b:
            return '0'
        return '1'


    def coder_table(self,Gx, Px, GxXn):
        print('-----Table-----')
        print('Gx', Gx)
        print('Px', Px)
        print('GxXn', GxXn)

        impuls = self.get_Gx_impulses(Gx, GxXn)

        coder = []

        coder.append(self.get_Px_coder(Px))

        for element in range(self.biggest_degree(GxXn)+1):
            filler = []
            for filler_element in range(len(self.get_Px_coder(Px))):
                filler.append(' ')
            coder.append(filler)

        # print(impuls, len(impuls))
        # print(1)
        # show_coder(coder)

        for i in range(1, self.biggest_degree(GxXn)+2):
            coder[i][0] = impuls[i-1]

        # print(2)
        # show_coder(coder)

        coder[1][0] = str(impuls[0]) + 'xor0'
        for i in range(1, len(self.get_Px_coder(Px))):
            if coder[0][i] == 'XOR':
                coder[1][i] = '0xor0'
            else:
                coder[1][i] = '0'

        # print(3)
        # show_coder(coder)

        for i in range(len(self.get_Px_coder(Px))):
            if 'xor' in str(coder[1][i]):
                coder[1][i+1] = self.XOR(int(coder[1][i][0]), int(coder[1][i][-1]))
                # print(coder[1][i+1])
            elif ' ' in str(coder[1][i]):
                coder[1][i] = '0'

        # print(4)
        # show_coder(coder)

        for i in range(len(self.get_Px_coder(Px))):
            if 'xor' in str(coder[1][i]):
                coder[1][i+1] = self.XOR(int(coder[1][i][0]), int(coder[1][i][-1]))
                # print(coder[1][i+1])
            elif ' ' in str(coder[1][i]):
                coder[1][i] = '0'

    # print(5)
    # show_coder(coder)

        for row in range(2, self.biggest_degree(GxXn)+2):
            last_impuls = coder[row-1][-1]
            for element in range(len(self.get_Px_coder(Px))):
                if coder[0][element] == 'XOR':
                    coder[row][element] = str(coder[row][element]) + f'xor{last_impuls}'
                    # print(coder[row])
                    coder[row][element+1] = self.XOR(int(coder[row][element][0]), int(coder[row][element][-1]))
                else:
                    if element < len(self.get_Px_coder(Px))-1:
                        coder[row][element+1] = str(coder[row-1][element])

        # print(6)
        # show_coder(coder)
        return coder


    def Rx_from_coder(self,coder):
        NAME_ROW = coder[0]
        LAST_ROW = coder[-1]
        Rx = ''
        for element in range(len(LAST_ROW)-1, -1, -1):
            if 'xor' in LAST_ROW[element]:
                continue
            else:
                Rx = Rx + NAME_ROW[element] + '+'
        Rx = Rx[:len(Rx)-1]
        return Rx


    def decoder_table(self,decoder):
        pass


    def main(self, G, P):
        ## print('Введите требуемые формулы по типу: "X4+X2+X1+1"')

        '''
        Gx = input('Введите G(x) (сообщение) ').upper()
        while not checkPxGx(Gx):
            Gx = input('Введите G(x) (сообщение) ').upper()
        Gx = Gx.split('+')

        print("Gx ", Gx)

        Px = input('Введите P(x) (полином) ').upper()
        while not checkPxGx(Px, 'Px'):
            Px = input('Введите P(x) (полином) ').upper()
        Px = Px.split('+')
        '''


        self.Gx = G #задается Gx

        self.Px = P #задается Px

        self.GxXn = self.mult_expression_on_biggerst_degree(self.Gx, self.Px)

        print("GxXn ", self.GxXn)

        self.Rx, self.Cx = self.GxXn_div_Px(self.GxXn, self.Px)

        print('-----Rx and Cx-----')
        print('Rx ', self.Rx)
        print('Cx ', self.Cx)

        self.Rx_, self.Px_ = self.GxXnRx_div_Cx(self.GxXn, self.Rx, self.Cx)

        print('-----Rx_ and Cx_-----')
        print('Rx_ ', self.Rx_)
        print('Px_ ', self.Px_)

        self.coder = self.coder_table(self.Gx, self.Px, self.GxXn)

        self.show_coder(self.coder)

        print('coder Rx ', self.Rx_from_coder(self.coder))


        return [self.Rx, self.Cx, self.Rx_, self.Px_, self.coder] #ыыыыыыыыыыыыыы

if __name__ == '__main__':
    a = CycleCoding()
    #                       G(x)                        P(x)
    b = a.main(['X9', 'X6', 'X5', 'X4', 'X2', '1'],['X4', 'X2', '1'])
    print(b)
