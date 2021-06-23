from owner_modify import modify

def main():
    document_id = input("Please enter the document id you want to delete: ")
    modify(document_id, "delete")

if __name__ == "__main__":
    main()