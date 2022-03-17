import sqlite3
from sys import exit
import unicodedata

# 接続。なければDBを作成する。
conn = sqlite3.connect('phoneBook.db')

# カーソルを取得
c = conn.cursor()
# テーブルを作成
c.execute('CREATE TABLE phoneBook (id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, number STRING)')

#メイン
def main():
    while True:
        #メニュー画面の表示
        command_number = input('''
        番号を入力してください(半角)
        1:名前/電話番号を検索
        2:電話番号を登録
        3:電話番号を削除
        4:電話番号を一覧
        0:プログラムの終了
        -> '''[1:])

        #コマンドの実行
        if command_number == '0':   #プログラムの終了
            # コミット これしないと登録が反映されない
            conn.commit()
            # コネクションをクローズ
            conn.close()
            exit('終了します')
        elif command_number == '1':
            p_search()
        elif command_number == '2':
            p_register()
        elif command_number == '3':
            p_remove()
        elif command_number == '4':
            p_display()
        else:
            print('0~4までの数字を半角で入力してください')


#名前、電話番号の検索
def p_search():
    NameorNum = input('名前か電話番号を入力してください -> ')
    #「-」やスペースを取り除く
    NameorNum = NameorNum.replace('-', '').replace('ー', '').replace(' ', '').replace('　', '')

    #入力が名前なのか、電話番号なのか判別しながら処理を行う
    try:
        int(NameorNum)
    except ValueError:
        #名前の場合
        # 調べる名前を全角に統一
        name = NameorNum.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)}))
        #チェック
        if name in phoneBook:
            print('{}の電話番号は{}です'.format(name, phoneBook[name]))
        else:
            print('{}という名前は電話帳に存在しません'.format(name))
            regi_answer = input('登録しますか？  はい/いいえ  ->  ')
            if regi_answer == 'はい':
                p_register()
    else:
        # 電話番号の場合
        # 調べる電話番号を半角に統一
        number = NameorNum.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
        #チェック
        if number in phoneBook.values():
            for key, value in phoneBook.items():
                if number == value:
                    print('{}は{}の電話番号です'.format(number, key))
        else:
            print('{}は電話帳にありません'.format(number))
            regi_answer = input('登録しますか？  はい/いいえ  ->  ')
            if regi_answer == 'はい':
                p_register()

#電話番号の登録
def p_register():
    #名前の登録
    regi_name = input('登録する名前を入力してください  ->  ')
    #名前は全角で統一
    regi_name = regi_name.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)}))

    #電話番号の登録
    regi_number = input('登録する電話番号を入力してください  ->  ')
    #不要な記号の除去
    regi_number = regi_number.replace('-', '').replace('ー', '').replace(' ', '').replace('　', '')

    #入力が適切な文字列なのか判定
    try:
        int(regi_number)
    except  ValueError:
        print('電話番号として不適切な文字列が入力されました\n再度入力してください')
    else:
        #電話番号は半角で統一
        regi_number = regi_number.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
        # Insert実行
        c.execute("INSERT INTO phoneBook (name,number) VALUES (regi_name,regi_number)")


    #データの更新
    #c.execute("UPDATE phoneBook SET number = ")



#電話番号の削除
def p_remove():
    rem_name = input('削除する名前を入力してください  ->  ')
    rem_name = rem_name.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)}))

    if rem_name in phoneBook:
        phoneBook.pop(rem_name, None)
        print('削除しました')
    else:
        print('{}という名前は電話帳に存在しません'.format(rem_name))

#電話番号の一覧表示
def p_display():
    for key,value in phoneBook.items():
        print('氏名：{0}　|  電話番号：{1} '.format(key,value))

if __name__ == '__main__':
    main()
