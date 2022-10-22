def QuitCommands(command):
    if command == 'q' or command == 'quit' or command == 'exit':
        return True
    else:
        return False

def Confirm_Data(data_dict):
    for key, value in data_dict.items():
        print(str(key) + ": " + str(value))