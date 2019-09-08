def process2Comp(string):
    if(string[0] == '1'):
        return -(15 - int(string,2) + 1)
    else:
        return int(string,2)


def simulate(memory,I):
    PC = 0
    IC = 0                             # PC
    Register = [ 0 for i in range(8)]        # Initialize register R0,R1,R2,R3,R4,R5,R6,R7
    finished = False
    print("*****************************")
    print("  Simulation started  ")
    print("*****************************")
    print()
    while(not(finished)):
        fetch = I[PC]
        if(fetch == "11111111"): # terminate
            finished = True
        elif(fetch[0:4] == "0100"): # INIT instruction

            imm = process2Comp(fetch[4:8])
            Register[0] = imm
            print ("PC "+str(PC)+" init " + str(imm))
            PC += 4
            IC += 1
        elif(fetch[0:4] == "0101"): # ADD instruction

            Rx = int(fetch[4:6],2)
            Ry = int(fetch[6:8],2)
            print ("PC "+str(PC)+" add R" + str(Rx) + ",R" + str(Ry))
            PC += 4
            IC += 1
            Register[Rx] = Register[Rx] + Register[Ry]

        elif(fetch[0:4] == "0110"): # split/div

            Rx = int(fetch[4:6],2)
            Ry = int(fetch[6:8],2)
            Register[Ry] = Register[0] & 0xFF
            Register[Rx] = Register[0] >> 8
            print ("PC "+str(PC)+" Split R" + str(Rx) + ",R" + str(Ry))
            PC += 4
            IC += 1

        elif(fetch[0:4] == "0111"): # ADDI
            Rx = int(fetch[4:6],2)
            imm = int(fetch[6:8],2)
            if (Rx == 0):
                Rx = 4
            Register[Rx] = Register[Rx] + imm
            print ("PC "+str(PC)+" addi R" + str(Rx) + "," + str(imm))
            PC += 4
            IC += 1

        elif(fetch[0:4] == "1100"): # SLT
            Rx = int(fetch[4:6],2)
            Ry = int(fetch[6:8],2)
            if (Rx == 0):           #if Rx or Ry == 00, then Rx or Ry = R4
               Rx = 4
            else:
               if (Ry == 0):
                   Ry = 4
            print ("PC "+str(PC)+" slt R" + str(Rx) + ",R" + str(Ry))
            PC += 4
            IC += 1
            if ( Register[Rx] < Register[Ry]):
                Register[0] = 1
            else:
                Register[0] = 0

        elif(fetch[0:4] == "1101"): # XOR
            Rx = int(fetch[4:6],2)
            Ry = int(fetch[6:8],2)
            print ("PC "+str(PC)+" xor R" + str(Rx) + ",R" + str(Ry))
            Register[Rx] = Register[Rx] ^ Register[Ry]
            PC += 4
            IC += 1

        elif(fetch[0:4] == "1110"): # DC
            Rx = int(fetch[4:6],2) #r1
            Ry = int(fetch[6:8],2)  #R3
            Register[0] = (Register[Rx] & 240) | (Register[Ry] & 15)
            print ("PC "+str(PC)+" dc R" + str(Rx) + ",R" + str(Ry))
            PC += 4
            IC += 1

        elif(fetch[0:4]=="0011"): #Mark
            Rx = int(fetch[4:8],2)
            print("PC "+ str(PC)+" Mark R"+str(Rx))
            Register[Rx] = PC + 4
            PC += 4
            IC += 1

        elif(fetch[0:4] == "0001"): # LOAD
            Rx = int(fetch[4:6],2)
            Ry = int(fetch[6:8],2)
            Register[Rx] = memory[Register[Ry]]
            print ("PC "+str(PC) +" load R" + str(Rx) + ",R" + str(Ry))
            PC += 4
            IC += 1

        elif(fetch[0:4] == "0000"): # STORE
            Rx = int(fetch[4:6],2)
            Ry = int(fetch[6:8],2)
            if (Rx == 0):  # if Rx or Ry == 00, then Rx or Ry = R4
                Rx = 4
            else:
                if (Ry == 0):
                    Ry = 4
            memory[Register[Ry]] = Register[Rx]
            print ( "PC "+str(PC) +" store R" + str(Rx) + ",R" + str(Ry))
            PC += 4
            IC += 1

        elif(fetch[0:4] == "1011"):   # BEQ
            Rx = int(fetch[4:5],2)
            imm = int(fetch[5:8],2)
            if (Register[Rx] == 0):
                print("PC "+ str(PC)+" beq R" + str(Rx) + "," + str(imm))
                PC = PC + 4 + (4*imm)
                IC += 1
            else:
                print("PC "+ str(PC)+" beq R" + str(Rx) + "," + str(imm))
                PC += 4
                IC += 1

        elif(fetch[0:4] == "0010"):  # Jump
            imm = int(fetch[4:8],2)
            print("PC "+str(PC)+" Jump R" + str(imm))
            PC = Register[imm]
            IC += 1

        elif(fetch[0:4] == "1000"): #Srl
            Rx = int(fetch[4:6],2)
            imm = int(fetch[6:8],2)
            print("PC " + str(PC)+ " srl R"+str(Rx)+",",str(imm))
            PC += 4
            Register[Rx]  = Register[Rx] >> imm
            IC += 1

        elif(fetch[0:4] == "1010"): #sub
            Rx = int(fetch[4:6],2)
            Ry = int(fetch[6:8],2)
            if (Rx == 2):
                Rx = 4
            if (Ry == 2):
                Ry = 4
            Register[Rx] = Register[Ry] - Register[Rx]
            print("PC "+ str(PC), " Sub R"+str(Rx) + ",R"+str(Ry))
            PC += 4
            IC += 1

        elif(fetch[0:4] == "1001"): #sand
            Rx = int(fetch[4:6],2)
            Ry = int(fetch[6:8],2)
            print("Value in Rx: ",Rx )
            print("Value in Ry: ", Ry)
            Register[Rx] = (Register[Ry] & 1 ) - 1
            print ("PC "+str(PC)+" sand R" + str(Rx) + ",R" + str(Ry))
            PC += 4
            IC += 1


        else:
            print("Instruction not supported. Exiting")
            exit()
    print()
    print("**********************************")
    print("Simulation Finished !!")
    print("**********************************")
    print()
    print("Registers Contents: ", Register)
    print()
    print()
    print("Memory Display", memory)
    print()
    print()
    print("Total Instruction Counts: ", IC)

def main():
    filename = "p3_g_8_prpg_s3.txt"
    print("Reading in machine code from " + filename)
    file = open(filename,"r")
    memory = [0 for i in range(64)]     # The memory of the machine
    I = []                                  # Instrucdtions to execute
    for line in file:
        if (line == "\n" or line[0] == "#" ):
            continue    # Skip empty lines and comments
        instr = bin(int(line[2:4],16))[2:].zfill(8)
        #  'zfill' pads the string with 0's to normalize instruction's length of 32
        I.append(instr)
        I.append(0)     # Since PC increments by 4,  let's fill
        I.append(0)     # null spaces with 0's to align correct
        I.append(0)     # address

    simulate(memory,I)
if __name__ == "__main__":
    main()
