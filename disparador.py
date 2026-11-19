 import os
import io
import re
import csv
import json
import time
import random
import urllib.parse
import requests

ID_PLANILHA      = "1T67ZMbIw_ynLmbGRnZckv41LfcUZUziavNAJh7rr0fQ"
WEBHOOK_PLANILHA = os.environ.get("WEBHOOK_PLANILHA", "")
TOKEN_SEGURANCA  = "NEOTRIBUTO2026"
CONTAS_SMTP_JSON = os.environ.get("CONTAS_SMTP_JSON", "[]")


def carregar_fila():
    dominio = "docs." + "google.com"
    caminho = "/spread" + "sheets/d/" + ID_PLANILHA + "/gviz/tq?tqx=out:csv&sheet=Leads"
    url_csv = "https://" + dominio + caminho
    resp = requests.get(url_csv, timeout=30)
    resp.encoding = "utf-8"
    leitor = csv.DictReader(io.StringIO(resp.text))

    fila = []
    for linha_num, row in enumerate(leitor, start=2):
        r = {str(k).strip().lower(): str(v or "").strip() for k, v in row.items() if k}
        empresa = r.get("empresa", "")
        cnpj = r.get("cnpj", "")
        email_raw = r.get("e-mail", "") or r.get("email", "")
        email = re.split(r"[,;]", email_raw)[0].strip().lower()
        st_email = r.get("status e-mail", "").lower()
        st_crm = r.get("status crm", "").lower()

        eh_mei = bool(re.search(r"\d{11}$", empresa) or re.match(r"^\d{2}\.\d{3}\.\d{3}", empresa))
        valido = ("v" in st_email and "lido" in st_email)

        if not eh_mei and st_crm == "novo" and valido and "@" in email and "." in email:
            fila.append({"linha": linha_num, "empresa": empresa, "cnpj": cnpj, "email": email})
            if len(fila) >= 60:
                break
    return fila


def montar_html(empresa, cnpj):
    ref = urllib.parse.quote(cnpj or empresa)
    s_sim = "neotributo.com.br/agendar?ref=" + ref
    s_wpp = "wa.me/551151977044?text=" + urllib.parse.quote(f"Simulacao gratuita para {empresa}")
    s_site = "neotributo.com.br"
    s_foto = "://githubusercontent.com"

    t = chr(60)
    f = chr(62)
    h = [
        f"{t}div style='font-family:Arial,sans-serif;max-width:620px;margin:auto;background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden'{f}",
        f"{t}div style='background:#071b33;padding:30px;color:#ffffff'{f}",
        f"{t}b style='font-size:20px;letter-spacing:1px'{f}NEOTRIBUTO{t}/b{f}",
        f"{t}h2 style='margin:14px 0 8px;font-size:22px'{f}Estimativa de economia tributaria para {empresa}{t}/h2{f}",
        f"{t}p style='margin:0;color:#cbd5e1;font-size:14px'{f}Operacoes administrativas de compensacao tributaria com seguranca juridica.{t}/p{f}",
        f"{t}/div{f}",
        f"{t}div style='padding:28px;color:#1e293b;font-size:15px;line-height:1.6'{f}",
        f"{t}p{f}Ola, {t}b{f}{empresa}{t}/b{f}.{t}/p{f}",
        f"{t}p{f}Empresas do {t}b{f}Lucro Real e Lucro Presumido{t}/b{f} costumam pagar ate {t}b{f}20% a mais em tributos federais{t}/b{f} do que o exigido pela legislacao atual.{t}/p{f}",
        f"{t}p{f}Na {t}b{f}NEOTRIBUTO{t}/b{f}, estruturamos compensacoes administrativas que geram alivio imediato de caixa sem acoes judiciais demoradas:{t}/p{f}",
        f"{t}ul style='background:#f8fafc;padding:16px 32px;border-left:4px solid #0e7490;border-radius:6px'{f}",
        f"{t}li{f}Recolhimento de R$ 100 mil/mes: economia estimada de {t}b{f}R$ 20.000/mes (R$ 240 mil/ano){t}/b{f}{t}/li{f}",
        f"{t}li{f}Recolhimento de R$ 500 mil/mes: economia estimada de {t}b{f}R$ 100.000/mes (R$ 1,2 milhao/ano){t}/b{f}{t}/li{f}",
        f"{t}li{f}Recolhimento de R$ 1 milhao/mes: economia estimada de {t}b{f}R$ 200.000/mes (R$ 2,4 milhoes/ano){t}/b{f}{t}/li{f}",
        f"{t}/ul{f}",
        f"{t}p{f}{t}b{f}Passivo Fiscal (PGFN):{t}/b{f} Tambem atuamos na negociacao, revisao de CAPAG e regularizacao de debitos inscritos na PGFN.{t}/p{f}",
        f"{t}p style='background:#eff6ff;padding:14px;border-radius:8px'{f}{t}b{f}Modelo 100% no exito:{t}/b{f} Zero custo antecipado para diagnostico e analise.{t}/p{f}",
        f"{t}img src='https://{s_foto}' style='width:100%;border-radius:8px;margin:12px 0'{f}",
        f"{t}p style='text-align:center;margin-top:20px'{f}{t}b{f}Responda OK a este e-mail ou acesse:{t}/b{f}{t}/p{f}",
        f"{t}p style='text-align:center'{f}",
        f"{t}a href='https://{s_sim}' style='display:inline-block;background:#0e7490;color:#fff;padding:12px 22px;text-decoration:none;border-radius:6px;font-weight:bold;margin:4px'{f}Solicitar Simulacao Gratuita{t}/a{f}",
        f"{t}a href='https://{s_wpp}' style='display:inline-block;background:#16a34a;color:#fff;padding:12px 22px;text-decoration:none;border-radius:6px;font-weight:bold;margin:4px'{f}Falar no WhatsApp{t}/a{f}",
        f"{t}a href='https://{s_site}' style='display:inline-block;background:#071b33;color:#fff;padding:12px 22px;text-decoration:none;border-radius:6px;font-weight:bold;margin:4px'{f}Site Oficial NEOTRIBUTO{t}/a{f}",
        f"{t}/p{f}",
        f"{t}/div{f}",
        f"{t}div style='background:#071b33;padding:20px;color:#94a3b8;font-size:12px;text-align:center'{f}",
        f"NEOTRIBUTO | Vitoria - Brasilia - Sao Paulo | WhatsApp: +55 (11) 5197-7044 | contato@neotributo.com.br",
        f"{t}/div{f}",
        f"{t}/div{f}"
    ]
    return "".join(h)


def executar():
    contas = json.loads(CONTAS_SMTP_JSON)
    fila = carregar_fila()
    print(f"Leads carregados da planilha: {len(fila)}")

    idx = 0
    for conta in contas:
        if idx >= len(fila):
            break
        user = conta["email"]
        url = conta["url"]
        limite = int(conta.get("limite_hora", 2))
        enviados = 0

        while enviados < limite and idx < len(fila):
            lead = fila[idx]
            idx += 1
            assunto = f"Estimativa de economia tributaria para {lead['empresa']}"
            payload = json.dumps({
                "token": TOKEN_SEGURANCA,
                "para": lead["email"],
                "assunto": assunto,
                "html": montar_html(lead["empresa"], lead["cnpj"])
            })
            cab = {"Content-Type": "text/plain;charset=utf-8"}
            r = requests.post(url, data=payload, headers=cab, timeout=25)

            if "OK" in r.text:
                requests.post(WEBHOOK_PLANILHA, json={
                    "token": TOKEN_SEGURANCA,
                    "linha": lead["linha"],
                    "conta": user
                }, timeout=15)
                enviados += 1
                print(f"[{user}] Enviado ({enviados}/{limite}) -> {lead['empresa']}")
                time.sleep(random.uniform(3.0, 6.0))
            elif "Invalid email" in r.text:
                print(f"Email invalido na linha {lead['linha']}: {lead['email']}")
                requests.post(WEBHOOK_PLANILHA, json={
                    "token": TOKEN_SEGURANCA,
                    "linha": lead["linha"],
                    "conta": "Erro E-mail"
                }, timeout=15)
            else:
                print(f"Conta {user} pausada: {r.text[:100]}")
                break


if __name__ == "__main__":
    executar()
