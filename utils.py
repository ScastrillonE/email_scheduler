def divide_list_email(lista):
    lista = [lista]
    limit = 40
    divided = 40
    list_finally = []
    for item in range(0, len(lista)):
        if len(lista[item]) > limit:
            def final_list(lista, x): return [
                lista[item][i:i+x] for i in range(0, len(lista[item]), x)]
            list_two = final_list(lista, divided)
            for itemm in range(0, len(list_two)):
                list_finally.append(list_two[itemm])
        else:
            return lista
    return list_finally
