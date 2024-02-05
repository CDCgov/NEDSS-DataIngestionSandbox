from typing import Dict

from .. import Provider as LoremProvider


class Provider(LoremProvider):
    """Implement lorem provider for ``hy_AM`` locale.

    Sources:

    - https://www.101languages.net/armenian/armenian-word-list
    """

    word_list = (
        "ես",
        "դու",
        "նա",
        "մենք",
        "դուք",
        "նրանք",
        "այս",
        "այն",
        "այստեղ",
        "այնտեղ",
        "ով",
        "ինչ",
        "որտեղ",
        "ուր",
        "երբ",
        "ինչպես",
        "ոչ",
        "բոլոր",
        "շատ",
        "որոշ",
        "քիչ",
        "այլ",
        "ուրիշ",
        "մեկ",
        "երկու",
        "երեք",
        "չորս",
        "հինգ",
        "մեծ",
        "երկար",
        "լայն",
        "հաստ",
        "ծանր",
        "փոքր",
        "կարճ",
        "նեղ",
        "բարակ",
        "կին",
        "տղամարդ",
        "մարդ",
        "երեխա",
        "կին",
        "ամուսին",
        "մայր",
        "հայր",
        "կենդանի",
        "ձուկ",
        "թռչուն",
        "շուն",
        "ոջիլ",
        "օձ",
        "ճիճու",
        "ծառ",
        "անտառ",
        "փայտ",
        "պտուղ",
        "սերմ",
        "տերև",
        "արմատ",
        "կեղև",
        "ծաղիկ",
        "խոտ",
        "պարան",
        "մաշկ",
        "կաշի",
        "միս",
        "արյուն",
        "ոսկոր",
        "ճարպ",
        "ձու",
        "եղջյուր",
        "պոզ",
        "պոչ",
        "փետուր",
        "մազ",
        "գլուխ",
        "ականջ",
        "աչք",
        "քիթ",
        "բերան",
        "ատամ",
        "լեզու",
        "եղունգ",
        "ոտք",
        "ծունկ",
        "ձեռք",
        "թև",
        "փոր",
        "փորոտիք",
        "աղիք",
        "վիզ",
        "մեջք",
        "կուրծք",
        "սիրտ",
        "լյարդ",
        "խմել",
        "ուտել",
        "կծել",
        "ծծել",
        "թքել",
        "ործկալ",
        "փչել",
        "շնչել",
        "ծիծաղել",
        "տեսնել",
        "լսել",
        "իմանալ",
        "գիտենալ",
        "մտածել",
        "զգալ",
        "վախենալ",
        "քնել",
        "ապրել",
        "մեռնել",
        "սպանել",
        "կռվել",
        "որսալ",
        "խփել",
        "հարվածել",
        "կտրել",
        "բաժանել",
        "խոցել",
        "քերծել",
        "քորել",
        "փորել",
        "լողալ",
        "թռչել",
        "քայլել",
        "գալ",
        "պառկել",
        "նստել",
        "կանգնել",
        "շրջվել",
        "ընկնել",
        "տալ",
        "պահել",
        "բռնել",
        "սեղմել",
        "շփել",
        "լվալ",
        "սրբել",
        "ձգել",
        "քաշել",
        "հրել",
        "նետել",
        "կապել",
        "կարել",
        "հաշվել",
        "ասել",
        "երգել",
        "խաղալ",
        "լողալ",
        "հոսել",
        "սառչել",
        "ուռել",
        "արև",
        "լուսին",
        "աստղ",
        "ջուր",
        "անձրև",
        "գետ",
        "լիճ",
        "ծով",
        "աղ",
        "քար",
        "ավազ",
        "փոշի",
        "հող",
        "ամպ",
        "մառախուղ",
        "մշուշ",
        "երկինք",
        "քամի",
        "ձյուն",
        "սառույց",
        "ծուխ",
        "հուր",
        "կրակ",
        "մոխիր",
        "վառվել",
        "այրվել",
        "ճամփա",
        "ճանապարհ",
        "լեռ",
        "սար",
        "կարմիր",
        "կանաչ",
        "դեղին",
        "սպիտակ",
        "սև",
        "գիշեր",
        "օր",
        "տարի",
        "տաք",
        "ցուրտ",
        "լիքը",
        "նոր",
        "հին",
        "լավ",
        "վատ",
        "փտած",
        "կեղտոտ",
        "ուղիղ",
        "կլոր",
        "սուր",
        "բութ",
        "հարթ",
        "թաց",
        "չոր",
        "ճիշտ",
        "մոտ",
        "հեռու",
        "աջ",
    )

    parts_of_speech: Dict[str, tuple] = {}
