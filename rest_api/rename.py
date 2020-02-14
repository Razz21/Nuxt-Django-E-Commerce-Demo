# importing os module
import os

def main():
    path = "C:\\Users\\ja\\Downloads\\images"
    count = 1

    for root, dirs, files in os.walk(path):
        for i in files:
            os.rename(os.path.join(root, i), os.path.join(root, "image" + str(count) + ".jpg"))
            count += 1


if __name__ == '__main__':
    main()