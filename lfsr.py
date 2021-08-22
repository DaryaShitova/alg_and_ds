class Lfsr():

    def __init__(self):
        """default constructor"""
        self.lfsr1 = [i for i in range(19)]
        self.lfsr2 = [i for i in range(22)]
        self.lfsr3 = [i for i in range(23)]

    def a5_rand(self):
        """Method "a5_rand" to calculate and return a random number according to the requested algorithm
        :return int
        """
        #Linking the three leftmost values with XOR to create a random number to be returned
        random_number = self.lfsr1[18] ^ self.lfsr2[21] ^ self.lfsr3[22]

        #Creating and inserting a new value in self.lfsr1[0], thus shifting the array
        new_lfsr1 = ((self.lfsr1[18] ^ self.lfsr1[17]) ^ self.lfsr1[16]) ^ self.lfsr1[13]
        new_lfsr1 = [new_lfsr1]
        self.lfsr1 = new_lfsr1 + self.lfsr1[:-1]

        # Creating and inserting a new value in self.lfsr2[0], thus shifting the array
        new_lfsr2 = self.lfsr2[21] ^ self.lfsr2[19]
        new_lfsr2 = [new_lfsr2]
        self.lfsr2 = new_lfsr2 + self.lfsr2[:-1]

        # Creating and inserting a new value in self.lfsr3[0], thus shifting the array
        new_lfsr3 = ((self.lfsr3[22] ^ self.lfsr3[21]) ^ self.lfsr3[15]) ^ self.lfsr3[7]
        new_lfsr3 = [new_lfsr3]
        self.lfsr3 = new_lfsr3 + self.lfsr3[:-1]

        return random_number

    def get_lfsr1(self):
        """Method "get_lfsr1" to return the content of the LFSR1 as an integer array
        :return int array
        """
        return self.lfsr1

    def get_lfsr2(self):
        """Method "get_lfsr2" to return the content of the LFSR2 as an integer array
        :return int array
        """
        return self.lfsr2

    def get_lfsr3(self):
        """Method "get_lfsr3" to return the content of the LFSR3 as an integer array
        :return int array
        """
        return self.lfsr3