import pandas as pd
from typing import Optional

def get_category(item_id: str) -> Optional[str]:

    try:
        supplier_df = pd.read_excel('data/Данные поставщика.xlsx')
        category_tree_df = pd.read_excel('data/Дерево категорий.xlsx')

        if supplier_df['Код артикула'].dtype == 'int64':
            item_id = int(item_id)
        
        item_row = supplier_df[supplier_df['Код артикула'] == item_id]
        
        if item_row.empty:
            print(f"Товар с ID {item_id} не найден в данных поставщика")
            return None
        
        name_words = item_row.iloc[0]['Название'].lower().split(',')[0].split()
        print(f"Название товара: {item_row.iloc[0]['Название']}")
        print(f"Разбитые слова: {name_words}")

        for _, cat_row in category_tree_df.iterrows():
            cat3_words = str(cat_row['cat_3']).lower().split()

            if len(cat3_words) == 1 or len(name_words) == 1:
                if name_words[0] == cat3_words[0]:
                    return cat_row['cat_id']
            else:
                if name_words[:2] == cat3_words[:2]:
                    return cat_row['cat_id']
        
        print("Подходящая категория не найдена")
        return None

    except Exception as e:
        print(f"Ошибка при определении категории: {e}")
        print(f"Детали ошибки: {str(e)}")
        return None

def check_product_category(item_id: str) -> None:

    try:
        products_df = pd.read_excel('data/Список товаров.xlsx')
        
        if products_df['item_id'].dtype == 'int64':
            item_id = int(item_id)
        
        row = products_df[products_df['item_id'] == item_id]
        
        if row.empty:
            print(f"Товар с ID {item_id} не найден в списке товаров")
            return
            
        expected_cat_id = row.iloc[0]['cat_id']
        actual_cat_id = get_category(str(item_id))
        
        if actual_cat_id is None:
            print(f"Не удалось определить категорию для товара {item_id}")
            return
            
        if expected_cat_id == actual_cat_id:
            print(f"Товар {item_id} соответствует ожидаемой категории: {expected_cat_id}")
        else:
            print(f"Товар {item_id} не соответствует ожидаемой категории")
            print(f"Ожидалось: {expected_cat_id}")
            print(f"Получено: {actual_cat_id}")
            
    except Exception as e:
        print(f"Ошибка при проверке категории: {e}")
        print(f"Детали ошибки: {str(e)}")

def main() -> None:

    try:
        while True:
            try:
                item_id = input("\nВведите ID товара (или 'q' для выхода): ")
                
                if item_id.lower() == 'q':
                    print("Программа завершена")
                    break
                    
                item_id = str(item_id).strip()
                if not item_id:
                    print("ID товара не может быть пустым")
                    continue
                    
                print(f"\nТестируем товар с ID: {item_id}")
                check_product_category(item_id)
                
            except ValueError:
                print("Пожалуйста, введите корректный ID товара")
                continue
                
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()