def find_combinations(tableaux, current_sum, current_combination, target_sum):
    combinations = []
    # Si la somme de la combinaison actuelle est égale à la somme cible
    if current_sum == target_sum:
        combinations.append(current_combination)
    # Si la somme de la combinaison actuelle est inférieure à la somme cible
    elif current_sum < target_sum:
        # Si tous les tableaux ont été explorés
        if len(tableaux) == 0:
            return []
        else:
            # Pour chaque élément du premier tableau
            for element in tableaux[0]:
                # Ajouter l'élément actuel à la combinaison
                new_combination = current_combination + [element]
                # Ajouter la valeur de l'élément actuel à la somme
                new_sum = current_sum + element
                # Appeler récursivement la fonction en utilisant les tableaux restants,
                # la nouvelle somme et la nouvelle combinaison
                combinations += find_combinations(tableaux[1:], new_sum, new_combination, target_sum)
    return combinations

tableau1 = [1, 2, 3, 4, 5]
tableau2 = [4, 5, 6, 7, 8]
tableau3 = [7, 8, 9, 10, 11]

tableaux = [tableau1, tableau2, tableau3]
target_sum = 20

print(find_combinations(tableaux, 0, [], target_sum))