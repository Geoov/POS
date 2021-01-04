Nu stiu daca e complet pentru ca l-am rescris la lab 8-9. Asta e dintr-o arhiva de backup

Atentie la linkuri sa fie cele care trebuie:

- din cererile postman(3 la numar)
- cel care e in endpoint
- cel din xsd
- cel din suprascrierea clasei WebServiceConfig.

Clasa WebServiceConfig suprascrie definitia WSDL ca sa ii dati voi url unde se va face cererea si catre ce namespace.

---

N-am mai facut alt ss, da cand faceti cererea in POSTMAN, la headers sa mai adaugati:

Content-Type: text/xml !!

Eu mai am inca 2:
Connection: close
nu cred ca trebuie neaparat

Cache-Control: no-cache


Multe clase nu-si au rostul, deci nu cred ca are rost sa le mai scrieti. Am incercat sa fac prostia aia de env-fault..

---

Primul pas ar trebuie sa fie sa creati elementele din xsd. (La mine se cheama login.xsd)

In pom sa aveti aceleasi dependinte ca mine. Daca totul e ok ar trebui ca puteti genera clase in functie de elementele din xsd.

Generarea claselor:

Accesati meniul de Maven -> Plugins -> jaxb2 -> jaxb2:xjc. Si in target se genereaza toate clasele. Adio erori



De aici doar faceti cateva teste cu postman si cam aia e.
