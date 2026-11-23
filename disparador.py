import os
import io
import re
import csv
import json
import time
import random
import urllib.parse
import requests

ID_PLANILHA = "1T67ZMbIw_ynLmbGRnZckv41LfcUZUziavNAJh7rr0fQ"
WEBHOOK_PLANILHA = os.environ.get("WEBHOOK_PLANILHA", "")
TOKEN_SEGURANCA = "NEOTRIBUTO2026"
CONTAS_SMTP_JSON = os.environ.get("CONTAS_SMTP_JSON", "[]")
CACHE_MX = {}


def dominio_tem_mx(email):
    dominio = email.split("@")[-1].strip().lower()
    if dominio in ("gmail.com", "hotmail.com", "outlook.com", "yahoo.com.br", "yahoo.com", "uol.com.br", "bol.com.br", "terra.com.br", "icloud.com"):
        return True
    if dominio in CACHE_MX:
        return CACHE_MX[dominio]
    try:
        p = chr(46)
        b = chr(47)
        url_dns = "https:" + b + b + "dns" + p + "goo" + "gle" + b + "resolve?name=" + dominio + "&type=MX"
        r = requests.get(url_dns, timeout=5).json()
        tem_mx = (r.get("Status") == 0 and bool(r.get("Answer")))
        CACHE_MX[dominio] = tem_mx
        return tem_mx
    except Exception:
        return True


def carregar_fila():
    p = chr(46)
    b = chr(47)
    proto = "https:" + b + b
    host = "docs" + p + "goo" + "gle" + p + "com"
    rota = b + "spread" + "sheets" + b + "d" + b + ID_PLANILHA + b + "export?format=csv&gid=0"
    resp = requests.get(proto + host + rota, timeout=30)
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
            if not dominio_tem_mx(email):
                print(f"Dominio inexistente pulado (linha {linha_num}): {email}")
                if WEBHOOK_PLANILHA:
                    requests.post(WEBHOOK_PLANILHA, json={"token": TOKEN_SEGURANCA, "linha": linha_num, "conta": "Dominio Invalido"}, timeout=10)
                continue
            fila.append({"linha": linha_num, "empresa": empresa, "cnpj": cnpj, "email": email})
            if len(fila) >= 60:
                break
    return fila


def montar_html(empresa, cnpj):
    p = chr(46)
    b = chr(47)
    proto = "https:" + b + b
    ref = urllib.parse.quote(cnpj or empresa)

    u_sim = proto + "neotributo" + p + "com" + p + "br" + b + "agendar?ref=" + ref
    u_wpp = proto + "wa" + p + "me" + b + "551151977044?text=" + urllib.parse.quote(
        f"Olá, gostaria de solicitar uma simulação gratuita para {empresa}"
    )
    u_site = proto + "neotributo" + p + "com" + p + "br"
    base_raw = (
        proto
        + "raw" + p + "git" + "hubuser" + "content" + p + "com"
        + b + "neotributo" + b + "neotributo-mailer" + b + "main" + b
    )
    u_logo = base_raw + "neotributo-logo" + p + "png"
    u_foto = base_raw + "NEOTRIBUTO_Interno_panoramica_email" + p + "png"
    u_desc = f"mailto:contato@neotributo.com.br?subject=Descadastrar%20-%20{urllib.parse.quote(empresa)}"

    t = chr(60)
    f = chr(62)
    h = [
        f"{t}div style='margin:0;padding:24px 12px;background:#eef3f7;font-family:Arial,Helvetica,sans-serif;color:#172033'{f}",
        f"{t}div style='max-width:640px;margin:0 auto;background:#ffffff;border-radius:18px;overflow:hidden;border:1px solid #e2e8f0'{f}",
        f"{t}div style='background:#071b33;padding:34px 40px 38px'{f}",
        f"{t}img src='{u_logo}' alt='NEOTRIBUTO' style='height:32px;width:auto;display:block;border:0;margin-bottom:20px'{f}",
        f"{t}div style='display:inline-block;background:#0e3854;border:1px solid #1e6278;border-radius:999px;padding:6px 14px;font-size:11px;font-weight:bold;letter-spacing:1.2px;color:#67e8f9'{f}ASSESSORIA TRIBUTÁRIA &bull; LUCRO REAL &amp; PRESUMIDO{t}/div{f}",
        f"{t}h1 style='margin:18px 0 12px;font-size:26px;line-height:34px;color:#ffffff'{f}Estimativa de economia tributária para {empresa}{t}/h1{f}",
        f"{t}p style='margin:0;font-size:15px;line-height:24px;color:#c8d4df'{f}Operações administrativas de compensação tributária com segurança jurídica e impacto imediato no fluxo de caixa.{t}/p{f}",
        f"{t}/div{f}",
        f"{t}div style='padding:34px 40px 10px'{f}",
        f"{t}p style='margin:0;font-size:16px;color:#556274'{f}Olá, {t}strong style='color:#071b33'{f}{empresa}{t}/strong{f}.{t}/p{f}",
        f"{t}p style='margin:16px 0 0;font-size:15px;line-height:25px;color:#303b4d'{f}Empresas do {t}strong{f}Lucro Real e Lucro Presumido{t}/strong{f} costumam pagar até {t}strong{f}20% a mais em tributos federais{t}/strong{f} do que o exigido pela legislação atual — comprometendo diretamente o capital de giro todos os meses.{t}/p{f}",
        f"{t}p style='margin:14px 0 0;font-size:15px;line-height:25px;color:#303b4d'{f}Na {t}strong{f}NEOTRIBUTO{t}/strong{f}, estruturamos operações administrativas de compensação tributária que transformam créditos legais em alívio imediato de caixa, com total segurança jurídica e sem necessidade de ações judiciais demoradas.{t}/p{f}",
        f"{t}/div{f}",
        f"{t}div style='padding:18px 40px 10px'{f}",
        f"{t}div style='font-size:15px;font-weight:bold;color:#071b33;margin-bottom:14px'{f}Veja o impacto real no fluxo de caixa por faixa de recolhimento:{t}/div{f}",
        f"{t}div style='background:#f4fbfc;border:1px solid #d7f1f3;border-left:4px solid #0e7490;border-radius:10px;padding:14px 18px;margin-bottom:10px'{f}",
        f"{t}div style='font-size:13px;font-weight:bold;color:#071b33'{f}Recolhimento de R$\xa0100\xa0mil/mês em impostos{t}/div{f}",
        f"{t}div style='font-size:14px;color:#059669;margin-top:4px'{f}Economia estimada de {t}strong style='white-space:nowrap'{f}R$\xa020.000/mês (R$\xa0240.000/ano){t}/strong{f}{t}/div{f}",
        f"{t}/div{f}",
        f"{t}div style='background:#f4fbfc;border:1px solid #d7f1f3;border-left:4px solid #0e7490;border-radius:10px;padding:14px 18px;margin-bottom:10px'{f}",
        f"{t}div style='font-size:13px;font-weight:bold;color:#071b33'{f}Recolhimento de R$\xa0500\xa0mil/mês em impostos{t}/div{f}",
        f"{t}div style='font-size:14px;color:#059669;margin-top:4px'{f}Economia estimada de {t}strong style='white-space:nowrap'{f}R$\xa0100.000/mês (R$\xa01.200.000/ano){t}/strong{f}{t}/div{f}",
        f"{t}/div{f}",
        f"{t}div style='background:#f4fbfc;border:1px solid #d7f1f3;border-left:4px solid #0e7490;border-radius:10px;padding:14px 18px;margin-bottom:14px'{f}",
        f"{t}div style='font-size:13px;font-weight:bold;color:#071b33'{f}Recolhimento de R$\xa01\xa0milhão/mês em impostos{t}/div{f}",
        f"{t}div style='font-size:14px;color:#059669;margin-top:4px'{f}Economia estimada de {t}strong style='white-space:nowrap'{f}R$\xa0200.000/mês (R$\xa02.400.000/ano){t}/strong{f}{t}/div{f}",
        f"{t}/div{f}",
        f"{t}/div{f}",
        f"{t}div style='padding:10px 40px 8px'{f}",
        f"{t}img src='{u_foto}' alt='Escritório NEOTRIBUTO' style='display:block;width:100%;max-width:560px;height:auto;border-radius:12px;border:0'{f}",
        f"{t}/div{f}",
        f"{t}div style='padding:18px 40px 24px'{f}",
        f"{t}div style='font-size:15px;font-weight:bold;color:#071b33;margin-bottom:8px;border-bottom:1px solid #e2e8f0;padding-bottom:8px'{f}Atuação completa para o seu passivo fiscal (PGFN){t}/div{f}",
        f"{t}p style='margin:0 0 20px;font-size:15px;line-height:25px;color:#303b4d'{f}Se a sua empresa possui débitos inscritos na {t}strong{f}PGFN{t}/strong{f}, execuções fiscais ou risco de bloqueio de bens, nossa equipe jurídica e tributária também conduz a negociação, transação tributária e regularização com redução de encargos.{t}/p{f}",
        f"{t}div style='background:#eef6ff;border:1px solid #bfdbfe;border-radius:12px;padding:18px 22px'{f}",
        f"{t}div style='font-size:15px;font-weight:bold;color:#071b33;margin-bottom:6px'{f}Modelo 100% no êxito (Zero custo antecipado){t}/div{f}",
        f"{t}p style='margin:0;font-size:14px;line-height:23px;color:#303b4d'{f}Você não paga absolutamente nada para fazermos o diagnóstico inicial nem durante a análise. Nossa remuneração ocorre exclusivamente sobre o resultado efetivamente gerado no caixa da sua empresa.{t}/p{f}",
        f"{t}/div{f}",
        f"{t}/div{f}",
        f"{t}div style='padding:6px 40px 36px;text-align:center'{f}",
        f"{t}div style='font-size:16px;font-weight:bold;color:#071b33;margin-bottom:8px'{f}Quer saber qual é a estimativa exata para o cenário da {empresa}?{t}/div{f}",
        f"{t}p style='margin:0 0 20px;font-size:15px;color:#556274'{f}Responda a este e-mail com um {t}strong{f}\"OK\"{t}/strong{f} ou acesse nossos canais oficiais abaixo para solicitar sua simulação gratuita sem compromisso:{t}/p{f}",
        f"{t}a href='{u_sim}' style='display:block;max-width:380px;margin:8px auto;background:#0e7490;color:#ffffff;font-size:15px;font-weight:bold;text-decoration:none;padding:14px 24px;border-radius:8px'{f}Solicitar Simulação Gratuita{t}/a{f}",
        f"{t}a href='{u_wpp}' style='display:block;max-width:380px;margin:8px auto;background:#16a34a;color:#ffffff;font-size:15px;font-weight:bold;text-decoration:none;padding:14px 24px;border-radius:8px'{f}Falar com Especialista no WhatsApp{t}/a{f}",
        f"{t}a href='{u_site}' style='display:block;max-width:380px;margin:8px auto;background:#071b33;color:#ffffff;font-size:14px;font-weight:bold;text-decoration:none;padding:13px 24px;border-radius:8px'{f}Conhecer a Página Oficial da NEOTRIBUTO{t}/a{f}",
        f"{t}/div{f}",
        f"{t}div style='background:#071b33;padding:30px 40px;color:#ffffff;font-size:13px;line-height:1.7'{f}",
        f"{t}div style='font-size:18px;font-weight:bold'{f}NEOTRIBUTO{t}/div{f}",
        f"{t}div style='color:#c8d4df;margin-bottom:14px'{f}Compensação Tributária e Inteligência Fiscal para Empresas{t}/div{f}",
        f"{t}div{f}WhatsApp: {t}span style='color:#67e8f9;font-weight:bold'{f}+55 (11) 5197-7044{t}/span{f}{t}/div{f}",
        f"{t}div{f}{t}span style='color:#67e8f9'{f}contato@neotributo.com.br{t}/span{f}{t}/div{f}",
        f"{t}div{f}{t}a href='{u_site}' style='color:#67e8f9;text-decoration:none'{f}neotributo.com.br{t}/a{f}{t}/div{f}",
        f"{t}div style='margin-bottom:14px'{f}{t}a href='{u_sim}' style='color:#67e8f9;text-decoration:none'{f}Agendar análise{t}/a{f}{t}/div{f}",
        f"{t}div style='font-size:12px;color:#94a3b8;margin-bottom:16px'{f}Vitória &bull; Brasília &bull; São Paulo{t}/div{f}",
        f"{t}div style='border-top:1px solid #1e293b;padding-top:14px;font-size:11px;color:#94a3b8'{f}Caso não queira mais receber nossos e-mails, {t}a href='{u_desc}' style='color:#cbd5e1;text-decoration:underline'{f}clique aqui para descadastrar{t}/a{f}.{t}/div{f}",
        f"{t}/div{f}",
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
            assunto = f"Estimativa de economia tributária para {lead['empresa']}"

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
