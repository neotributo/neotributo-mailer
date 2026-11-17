import os
import json
import time
import random
import urllib.parse
import requests

WEBHOOK_PLANILHA = os.environ.get("WEBHOOK_PLANILHA", "")
TOKEN_SEGURANCA  = "NEOTRIBUTO2026"
CONTAS_SMTP_JSON = os.environ.get("CONTAS_SMTP_JSON", "[]")

def montar_html(empresa, cnpj):
    ref = urllib.parse.quote(cnpj or empresa)
    link_sim  = "https://" + "neotributo.com.br/agendar?ref=" + ref
    link_wpp  = "https://" + "wa.me/551151977044?text=" + urllib.parse.quote(
        f"Olá, gostaria de solicitar uma simulação gratuita para {empresa}"
    )
    link_site = "https://" + "neotributo.com.br"
    foto_url  = "https://" + "raw." + "githubusercontent.com" + "/neotributo/neotributo-mailer/main/NEOTRIBUTO_Interno_panoramica_email.png"

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#eef3f7;font-family:Arial,Helvetica,sans-serif;color:#172033;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background:#eef3f7;">
    <tr><td align="center" style="padding:30px 12px;">
      <table role="presentation" width="640" cellspacing="0" cellpadding="0" border="0" style="width:100%;max-width:640px;background:#ffffff;border-radius:18px;overflow:hidden;">
        <tr><td style="background:#071b33;padding:34px 42px 38px;">
          <div style="font-size:22px;font-weight:bold;letter-spacing:1.5px;color:#ffffff;margin-bottom:20px;">NEOTRIBUTO</div>
          <div style="display:inline-block;background:#0e3854;border:1px solid #1e6278;border-radius:999px;padding:6px 14px;font-size:11px;font-weight:bold;letter-spacing:1.2px;color:#67e8f9;">ASSESSORIA TRIBUTÁRIA &bull; LUCRO REAL &amp; PRESUMIDO</div>
          <h1 style="margin:18px 0 12px;font-size:26px;line-height:34px;color:#ffffff;">Estimativa de economia tributária para {empresa}</h1>
          <p style="margin:0;font-size:15px;line-height:24px;color:#c8d4df;">Operações administrativas de compensação tributária com segurança jurídica e impacto imediato no fluxo de caixa.</p>
        </td></tr>
        <tr><td style="padding:34px 42px 10px;">
          <p style="margin:0;font-size:16px;color:#556274;">Olá, <strong style="color:#071b33;">{empresa}</strong>.</p>
          <p style="margin:16px 0 0;font-size:15px;line-height:25px;color:#303b4d;">Empresas do <strong>Lucro Real e Lucro Presumido</strong> costumam pagar até <strong>20% a mais em tributos federais</strong> do que o exigido pela legislação atual — comprometendo diretamente o capital de giro todos os meses.</p>
          <p style="margin:14px 0 0;font-size:15px;line-height:25px;color:#303b4d;">Na <strong>NEOTRIBUTO</strong>, estruturamos operações administrativas de compensação tributária que transformam créditos legais em alívio imediato de caixa, com total segurança jurídica e sem necessidade de ações judiciais demoradas.</p>
        </td></tr>
        <tr><td style="padding:18px 42px 10px;">
          <div style="font-size:15px;font-weight:bold;color:#071b33;margin-bottom:14px;">Veja o impacto real no fluxo de caixa por faixa de recolhimento:</div>
          <div style="background:#f4fbfc;border:1px solid #d7f1f3;border-left:4px solid #0e7490;border-radius:10px;padding:14px 18px;margin-bottom:10px;">
            <div style="font-size:13px;font-weight:bold;color:#071b33;">Recolhimento de R$ 100 mil/mês em impostos</div>
            <div style="font-size:14px;color:#059669;margin-top:4px;">Economia estimada de <strong>R$ 20.000/mês (R$ 240.000/ano)</strong></div>
          </div>
          <div style="background:#f4fbfc;border:1px solid #d7f1f3;border-left:4px solid #0e7490;border-radius:10px;padding:14px 18px;margin-bottom:10px;">
            <div style="font-size:13px;font-weight:bold;color:#071b33;">Recolhimento de R$ 500 mil/mês em impostos</div>
            <div style="font-size:14px;color:#059669;margin-top:4px;">Economia estimada de <strong>R$ 100.000/mês (R$ 1.200.000/ano)</strong></div>
          </div>
          <div style="background:#f4fbfc;border:1px solid #d7f1f3;border-left:4px solid #0e7490;border-radius:10px;padding:14px 18px;margin-bottom:14px;">
            <div style="font-size:13px;font-weight:bold;color:#071b33;">Recolhimento de R$ 1 milhão/mês em impostos</div>
            <div style="font-size:14px;color:#059669;margin-top:4px;">Economia estimada de <strong>R$ 200.000/mês (R$ 2.400.000/ano)</strong></div>
          </div>
        </td></tr>
        <tr><td style="padding:10px 42px 24px;">
          <div style="font-size:15px;font-weight:bold;color:#071b33;margin-bottom:8px;border-bottom:1px solid #e2e8f0;padding-bottom:8px;">Atuação completa para o seu passivo fiscal (PGFN)</div>
          <p style="margin:0 0 20px;font-size:15px;line-height:25px;color:#303b4d;">Se a sua empresa possui débitos inscritos na <strong>PGFN</strong>, execuções fiscais ou risco de bloqueio de bens, nossa equipe jurídica e tributária também conduz a negociação, transação tributária e regularização com redução de encargos.</p>
          <div style="background:#eef6ff;border:1px solid #bfdbfe;border-radius:12px;padding:18px 22px;">
            <div style="font-size:15px;font-weight:bold;color:#071b33;margin-bottom:6px;">Modelo 100% no êxito (Zero custo antecipado)</div>
            <p style="margin:0;font-size:14px;line-height:23px;color:#303b4d;">Você não paga absolutamente nada para fazermos o diagnóstico inicial nem durante a análise. Nossa remuneração ocorre exclusivamente sobre o resultado efetivamente gerado no caixa da sua empresa.</p>
          </div>
        </td></tr>
        <tr><td style="padding:18px 42px 8px;">
          <img src="{foto_url}" width="556" alt="Escritório NEOTRIBUTO" style="display:block;width:100%;max-width:556px;height:auto;border-radius:12px;border:0;">
        </td></tr>
        <tr><td style="padding:6px 42px 36px;text-align:center;">
          <div style="font-size:16px;font-weight:bold;color:#071b33;margin-bottom:8px;">Quer saber qual é a estimativa exata para o cenário da {empresa}?</div>
          <p style="margin:0 0 20px;font-size:15px;color:#556274;">Responda a este e-mail com um <strong>"OK"</strong> ou acesse nossos canais oficiais abaixo:</p>
          <a href="{link_sim}" style="display:block;max-width:380px;margin:8px auto;background:#0e7490;color:#ffffff;font-size:15px;font-weight:bold;text-decoration:none;padding:14px 24px;border-radius:8px;">Solicitar Simulação Gratuita</a>
          <a href="{link_wpp}" style="display:block;max-width:380px;margin:8px auto;background:#16a34a;color:#ffffff;font-size:15px;font-weight:bold;text-decoration:none;padding:14px 24px;border-radius:8px;">Falar com Especialista no WhatsApp</a>
          <a href="{link_site}" style="display:block;max-width:380px;margin:8px auto;background:#071b33;color:#ffffff;font-size:14px;font-weight:bold;text-decoration:none;padding:13px 24px;border-radius:8px;">Conhecer a Página Oficial da NEOTRIBUTO</a>
        </td></tr>
        <tr><td style="background:#071b33;padding:30px 42px;color:#ffffff;">
          <div style="font-size:18px;font-weight:bold;">NEOTRIBUTO</div>
          <div style="margin-top:4px;font-size:13px;color:#c8d4df;">Compensação Tributária e Inteligência Fiscal para Empresas</div>
          <div style="margin-top:14px;font-size:13px;color:#67e8f9;">WhatsApp: +55 (11) 5197-7044 &bull; contato@neotributo.com.br</div>
          <div style="margin-top:12px;font-size:12px;color:#94a3b8;">Vitória &bull; Brasília &bull; São Paulo</div>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""

def executar():
    contas = json.loads(CONTAS_SMTP_JSON)
    resp = requests.get(f"{WEBHOOK_PLANILHA}?action=fila_github&token={TOKEN_SEGURANCA}", timeout=30)
    fila_leads = resp.json()
    print(f"Leads carregados da planilha: {len(fila_leads)}")

    ponteiro = 0
    for conta in contas:
        if ponteiro >= len(fila_leads):
            break
        email_user  = conta["email"]
        url_disparo = conta["url"]
        limite_hora = int(conta.get("limite_hora", 2))
        enviados_conta = 0

        while enviados_conta < limite_hora and ponteiro < len(fila_leads):
            lead = fila_leads[ponteiro]
            ponteiro += 1
            assunto = f"Estimativa de economia tributária para {lead['empresa']}"
            payload = json.dumps({
                "token": TOKEN_SEGURANCA,
                "para": lead["email"],
                "assunto": assunto,
                "html": montar_html(lead["empresa"], lead["cnpj"])
            })
            r = requests.post(
                url_disparo,
                data=payload,
                headers={"Content-Type": "text/plain;charset=utf-8"},
                timeout=25
            )

            if "OK" in r.text:
                requests.post(WEBHOOK_PLANILHA, json={
                    "token": TOKEN_SEGURANCA,
                    "linha": lead["linha"],
                    "conta": email_user
                }, timeout=15)
                enviados_conta += 1
                print(f"[{email_user}] Enviado ({enviados_conta}/{limite_hora}) -> {lead['empresa']}")
                time.sleep(random.uniform(3.0, 6.0))
            else:
                print(f"Conta {email_user} pausada ou cota atingida: {r.text[:120]}")
                break

if __name__ == "__main__":
    executar()
