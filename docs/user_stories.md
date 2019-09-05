## Käyttötapaukset, ja niihin liittyvät routet & sql -kyselyt

### Käyttäjänä haluan rekisteröidä itselleni tilin

* route: /register
* sql -kyselyt:
  1. Tarkistetaan onko käyttäjänimellä olemassaolevaa käyttäjää
    ```
    SELECT account.id FROM account
    WHERE account.username = <username>
    ```
  2. Luodaan uusi käyttäjä
    ```
    INSERT INTO account (username, password)
    VALUES (<username>, <password>)
    ```

### Käyttäjäna haluan kirjautua tililleni

* route: /login
* sql -kyselyt:
  1. Haetaan käyttäjän tiedot
    ```
    SELECT * FROM account
    WHERE account.username = <username>
    AND account.password = <password>
    ```

### Käyttäjänä haluan kirjautua ulos tililtäni

* route: /logout

### Käyttäjänä haluan luoda palstoja

* route: /threads/new
* sql -kyselyt:
  1. Lisätään threadi
    ```
    INSERT INTO thread (title, content, author_id, locked)
    VALUES (<title>, <content>, <author_id>, <lock_status>)
    ```

### Käyttäjänä haluan luoda kommentteja palstoihin

* route: /thread/<thread_id>/
* sql -kyselyt:
  1. Lisätään kommentti
    ```
    INSERT INTO comment (author_id, thread_id, content)
    VALUES (<author_id>, <thread_id>, <content>)
    ```

### Käyttäjänä haluan nähdä kenen luomia kommentit ja palstat ovat

* route: /thread/<thread_id>/
* sql -kyselyt:
  1. Kenen luoma thread on
    ```
    SELECT account.username FROM thread
    JOIN account on thread.author_id = account.id
    WHERE thread.id = <thread_id>
    ```
  2. Kenen luoma kommentti on
    ```
    SELECT account.username FROM comment
    JOIN account on comment.author_id = account.id
    WHERE comment.id = <comment_id>
    ```
### Käyttäjänä haluan lukita/avata luomiani palstoja

* route: /threads/lock/<thread_id>/
* sql -kyselyt:
  1. Hae nykynen lukkotila
    ```
    SELECT thread.locked from thread
    WHERE thread.id=<thread_id>
    ```
  2. Tallenna uusi lukkotila
    ```
    UPDATE thread
    SET locked = <lock_value>
    WHERE thread.id=<thread_id>
    ```

### Käyttäjänä haluan muokata luomiani palstoja

* route: /thread/<thread_id>/m
* sql -kyselyt:
  1. Hae nykyinen thread
    ```
    SELECT thread.title, thread.content FROM thread
    WHERE thread.id=<thread_id>
    ```
  2. Tallenna muokattu thread
    ```
    UPDATE thread
    SET title=<new_title>, content=<new_content>
    WHERE thread.id=<thread_id>
    ```

### Käyttäjänä haluan muokata luomiani kommentteja

* route: /comments/<thread_id>/m
* sql -kyselyt:
  1. Hae nykyinen kommentti
    ```
    SELECT comment.content FROM comment
    WHERE comment.id=<comment_id>
    ```
  2. Tallenna muokattu kommentti
    ```
    UPDATE comment
    SET content=<new_content>
    WHERE comment.id=<comment_id>
    ```

### Käyttäjäna haluan poistaa luomiani palstoja

* route: /threads/delete/<thread_id>
* Autorisointitarkastus, chekataan onko käyttäjän id sama kuin threadin authorin id
* sql -kyselyt:
  1. Poista palstan kommenttien upvotet
    ```
    DELETE FROM upvote
    WHERE upvote.comment_id IN (
      SELECT upvote.comment_id FROM upvote
      JOIN comment
      ON comment.id=upvote.comment_id
      WHERE comment.thread_id=<thread_id>
      )

    ```
  2. Poista palstan kommentit
    ```
    DELETE FROM comment
    WHERE comment.thread_id=<thread_id>
    ```
  3. Poista palsta
    ```
    DELETE FROM thread
    WHERE thread_id=<thread_id>
    ```
### Käyttäjänä haluan poistaa omia kommenttejani palstoilta

* route /comment/delete/<comment_id>
* Autorisointitarkastus, chekataan onko kayttäjän id sama kuin kommentin authorin id
* sql -kyselyt:
  1. Poista kommentin upvotet:
    ```
    DELETE FROM upvote
    WHERE upvote.comment_id=<comment_id>
    ```

  2. Poista itse kommentti
    ```
    DELETE FROM comment
    WHERE comment.id=<comment_id>
    ```

### Käyttäjänä haluan poistaa kommentteja luomiltani palstoilta

* route /comment/delete/<comment_id>
* Chekataan onko kommentin thread_id:tä vastava thread
nykyisen käyttäjän luoma
* sql -kyselyt:
  * Samat kuin yllä

### Käyttäjänä haluan vaihtaa käyttäjänimeni & salasanani tai poistaa käyttäjäni

* route /user/<username>
* Chekataan onko nykyinen käyttäjä sama mitä muutetaan
* sql -kyselyt
  1. Jos muokataan käyttäjänimeä
    - Haetaan käyttäjän id
      ```
      SELECT account.id FROM account
      WHERE account.username=<username>
      ```
    - Päivitetään käyttäjänimi
      ```
      UPDATE account
      SET username=<new_username>
      WHERE account_id=<account_id>
      ```
  2. Jos muokataan salasanaa
    - Haetaan käyttäjän id
      ```
      SELECT account.id FROM account
      WHERE account.username=<username>
      ```
    - Päivitetään salasana
      ```
      UPDATE account
      SET password=<new_password>
      WHERE account_id=<account_id>
      ```
  3. Jos poistetaan käyttäjä
    - Haetaan käyttäjän id
      ```
      SELECT account.id FROM account
      WHERE account.username=<username>
      ```
    - Poistetaan kaikki käyttäjän upvotet
      ```
      DELETE FROM upvote
      WHERE upvote.author_id=<account_id>
      ```
    - Poistetaan kaikki käyttäjän kommentit
      ```
      DELETE FROM comment
      WHERE comment.author_id=<account_id>
      ```
    - Poistetaan kaikki kommentit käyttäjän luomilta palstoilta
      ```
      DELETE FROM comment
      WHERE comment.thread_id IN (
        SELECT comment.thread_id FROM comment
        JOIN thread
        ON comment.thread_id=thread.id
        WHERE thread.author_id=<account_id>
        )
      ```
    - Poistetaan kaikki käyttäjän palstat
      ```
      DELETE FROM thread
      WHERE thread.author_id=<account_id>
      ```

### Käyttäjänä haluan upvotee tai downvotee kommentteja

* route /comments/vote/<comment_id>/<is_up>
* sql -kyselyt:
  1. Tarkistetaan onko käyttäjä upvotennut aikaisemmin
  2. Tarkistetaan onko käyttäjä downvotennut aikaisemmin
  3. Tallennetaan uusi vote
    - Jos päivitetään aikaisempi vote
      ```
      UPDATE upvote
      SET is_up=<is_up>
      WHERE upvote.comment_id=<comment_id>, upvote.author_id=<account.id>
      ```
    - Jos luodaan uusi vote
      ```
      INSERT INTO upvote (comment_id, author_id, is_up)
      VALUES (<comment_id>, <author_id>, <is_up>)
      ```
### Käyttäjänä haluan nähdä käyttäjien upvote/downvote määrät

* route /user/<uname>
* sql -kyselyt
  1. Haetaan käyttäjän kommentien upvotet
    ```
    SELECT COUNT(upvote.is_up) FROM upvote
    JOIN comment ON comment.id=upvote.comment_id
    JOIN account on account.id=comment.author_id
    where upvote.is_up=1
    AND account.id=<account_id>
    ```
  2. Haetaan käyttäjän kommenttien downvotet
    ```
    SELECT COUNT(upvote.is_up) FROM upvote
    JOIN comment ON comment.id=upvote.comment_id
    JOIN account on account.id=comment.author_id
    where upvote.is_up=0
    AND account.id=<account_id>
    ```
