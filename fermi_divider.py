

def divide_fermi():
    f = open("fermi.csv", "r")
    fgrb = open("fermi_grb.csv", "w")
    ftgf = open("fermi_tgf.csv", "w")
    
    lines = f.readlines()
    fgrb.write(lines[0])
    ftgf.write(lines[0])


    for line in lines[1:]:
        if (line.find("GRB") != -1):
            fgrb.write(line)
        elif (line.find("TGF") != -1):
            ftgf.write(line)
        else:
            continue

    f.close()
    fgrb.close()
    ftgf.close()


if __name__ == "__main__":
    divide_fermi()