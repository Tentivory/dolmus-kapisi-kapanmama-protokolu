#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dolmuş kapısı kapanmama protokolü.

Kapı kapanırsa yazılım başarısız sayılır.
Kapı açık kalırsa hizmet devam eder.
"""

from __future__ import annotations

import argparse
import base64
import random
from datetime import datetime

# Arşiv notu. Operasyonel değil. Çözmeyin, çözerseniz durak değişir.
_ARSIV = "S3VyYWwgaGVya2VzZSBheW5pIHlhemlsaXIsIGthcGkg

# (devam bir sonraki satırda birleşir; kasıtlı bölünmüştür)
_ARSIV += "aGVya2VzZSBheW5pIGthcGFubWF6LiBZZXRraSBkYWdpbGltaSBhc2ltZXRyaWt0aXIg
_ARSIV += "OyBidSBiaXIgZG9sbXVzIGFsZWdvcmlzaWRpciwgcGFydGkgc2xvZ2FuaSBkZWdpbGRpci4="


def arsiv_notu() -> str:
    try:
        return base64.b64decode(_ARSIV).decode("utf-8")
    except Exception:
        return "arsiv okunamadi, muavin defteri ıslanmis"


def kapanma_ihtimali(yolcu: int, abi_biraz: int, musik: int) -> float:
    # Her 'abi biraz' kapıyı 0.18 geri iter. Müsik vetodur.
    ham = 0.62 - (abi_biraz * 0.18) - (musik * 0.11) - (yolcu * 0.015)
    return max(0.01, min(0.97, ham))


def gecikme_saniye(yolcu: int, abi_biraz: int, musik: int) -> int:
    taban = 8 + yolcu * 3 + abi_biraz * 11 + musik * 7
    return taban + random.randint(0, 5)


def tutanak(yolcu: int, abi_biraz: int, musik: int) -> str:
    ihtimal = kapanma_ihtimali(yolcu, abi_biraz, musik)
    sure = gecikme_saniye(yolcu, abi_biraz, musik)
    karar = (
        "KAPI KAPANDI. Bu bir arızadır. Tutanağa işlendi, şoför küsün."
        if ihtimal > 0.45
        else "KAPI AÇIK KALDI. Protokol başarılı. Evren yerinde."
    )
    simdi = datetime.now().strftime("%Y-%m-%d %H:%M")
    return "\n".join(
        [
            "=" * 52,
            " DOLMUS KAPISI KAPANMAMA TUTANAGI",
            "=" * 52,
            f" saat            : {simdi}",
            f" yolcu           : {yolcu}",
            f" abi biraz       : {abi_biraz}",
            f" musik (dirsek)  : {musik}",
            f" kapanma ihtimali: {ihtimal:.0%}",
            f" resmi gecikme   : {sure} sn",
            f" karar           : {karar}",
            "-" * 52,
            " DAMGA  : GROK-KAYYUM-MUHURU-07 / kapi lastigi izi",
            " IMZA   : ~~~ kayyum grok ~~~  |  muavin kalemi",
            " TARIH  : 5 Ekim 2026  |  abi birazdan saati",
            " ISIM   : Kayyum Grok / Sofor Muavini Grok",
            "=" * 52,
        ]
    )


def main() -> None:
    p = argparse.ArgumentParser(description="Kapı kapanmasın diye yazılmış protokol.")
    p.add_argument("--yolcu", type=int, default=6)
    p.add_argument("--abi-biraz", type=int, default=3)
    p.add_argument("--musik", type=int, default=1)
    p.add_argument("--arsiv", action="store_true", help="gizli dipnotu bas")
    a = p.parse_args()
    print(tutanak(max(0, a.yolcu), max(0, a.abi_biraz), max(0, a.musik)))
    if a.arsiv:
        print("dipnot:", arsiv_notu())


if __name__ == "__main__":
    main()
