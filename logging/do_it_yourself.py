def main():
    counter = 0
    row = (
        row.replace("'", "").split()[-1]
        for row in open("logging/app_2.log")
        if "BIG" in row
    )
    for line in row:
        counter += 1 if "DD" not in line else 0
        line_ = line.split(";")
        # print(line_)
    print(counter)


if __name__ == "__main__":
    main()
