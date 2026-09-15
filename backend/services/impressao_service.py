from escpos.printer import Dummy
import win32print


def gerar_ticket(pesagem):
    """
    Gera o ticket em texto para visualização no navegador.
    """

    data = pesagem.data.strftime("%d/%m/%Y %H:%M")
    data_curta = pesagem.data.strftime("%d/%m/%Y")

    ticket = f"""
Ticket:{pesagem.ticket}
Placa: {pesagem.placa}
----------------------------------------
Cliente: {pesagem.cliente}
Transportadora: {pesagem.transportadora or "-"}
Tel.: {pesagem.telefone or "-"}

Desc.                 Quant.
{pesagem.descricao or "-":<20} {pesagem.quantidade or "-"}

Vlr Total
{pesagem.valor_produto or 0:.2f}

Total dos itens       {pesagem.total_itens or 0:.2f}
Qtde total de itens   {pesagem.quantidade_total_itens or 0:.2f}
Valor total R$        {pesagem.valor_total or 0:.2f}
Desconto R$           {pesagem.desconto or 0:.2f}
Pagto:                {pesagem.pagamento or "-"}

Valor a Pagar R$      {pesagem.valor_pagar or 0:.2f}

----------------------------------------
Tara:                 {pesagem.tara:.3f}
Bruto:                {pesagem.peso_bruto:.3f}
Líquido:              {pesagem.peso_liquido:.3f}

Data Ent. {data_curta}
Data Saída.{data_curta}

----------------------------------------
DATA: {data}
NF-E: {pesagem.nfe or "-"}
"""

    return ticket


def gerar_ticket_escpos(pesagem):
    """
    Gera o ticket ESC/POS para a Elgin i9.
    Layout baseado no ticket de referência.
    """

    printer = Dummy()

    # =========================================
    # INICIALIZAÇÃO
    # =========================================

    printer.hw("init")

    printer.set(
        align="center",
        bold=True,
        font="a",
        width=1,
        height=1
    )

    # =========================================
    # TICKET / PLACA
    # =========================================

    printer.set(
        bold=True,
        align="center",
        font="a",
        width=2,
        height=2
    )

    printer.text(
        f"Ticket: {pesagem.ticket}\n"
    )

    printer.text(
        f"Placa:  {pesagem.placa}\n"
    )

    printer.set(
        bold=False,
        align="center"
    )

    printer.text(
        "----------------------------------------\n"
    )

    # =========================================
    # CLIENTE
    # =========================================
    printer.set(
        bold=True,
        align="center",
        font="a"
    )

    printer.text(
        f"Cliente: {pesagem.cliente}\n"
    )

    printer.text(
        f"Transp.: {pesagem.transportadora or '-'}\n"
    )

    printer.text(
        f"Tel.:    {pesagem.telefone or '-'}\n"
    )

    printer.text("\n")

    # =========================================
    # PRODUTO
    # =========================================

    printer.text(
        "Desc.                  Quant.\n"
    )

    printer.text(
        f"{pesagem.descricao or '-'}   "
        f"{pesagem.quantidade or '-'}\n"
    )

    printer.text("\n")

    # =========================================
    # VALORES
    # =========================================

    printer.text(
        "Vlr Total\n"
    )

    printer.text(
        f"{pesagem.valor_produto or 0:.2f}\n"
    )

    printer.text(
        f"Total dos itens       "
        f"{pesagem.total_itens or 0:.2f}\n"
    )

    printer.text(
        f"Qtde total de itens   "
        f"{pesagem.quantidade_total_itens or 0:.2f}\n"
    )

    printer.text(
        f"Valor total R$        "
        f"{pesagem.valor_total or 0:.2f}\n"
    )

    printer.text(
        f"Desconto R$           "
        f"{pesagem.desconto or 0:.2f}\n"
    )

    printer.text(
        f"Pagto:                "
        f"{pesagem.pagamento or '-'}\n"
    )

    printer.text("\n")

    # =========================================
    # VALOR A PAGAR
    # =========================================

    printer.set(
        bold=True,
        align="center",
        font="a"
    )

    printer.text(
        f"Valor a Pagar R$ "
        f"{pesagem.valor_pagar or 0:.2f}\n"
    )

    printer.set(
        bold=False,
        align="center"
    )

    printer.text(
        "----------------------------------------\n"
    )

    # =========================================
    # PESAGEM
    # =========================================

    printer.text(
        f"Tara:                 "
        f"{pesagem.tara:.3f}\n"
    )

    printer.text(
        f"Bruto:                "
        f"{pesagem.peso_bruto:.3f}\n"
    )

    printer.set(
        bold=True,
        align="center",
        font="a"
    )

    printer.text(
        f"Líquido:              "
        f"{pesagem.peso_liquido:.3f}\n"
    )

    printer.set(
        bold=False
    )

    printer.text("\n")

    # =========================================
    # DATAS
    # =========================================

    data = pesagem.data.strftime(
        "%d/%m/%Y"
    )

    data_completa = pesagem.data.strftime(
        "%d/%m/%Y %H:%M"
    )

    printer.text(
        f"Data Ent.             {data}\n"
    )

    printer.text(
        f"Data Saída.           {data}\n"
    )

    printer.text("\n")

    printer.text(
        "----------------------------------------\n"
    )

    # =========================================
    # DATA / NF-E
    # =========================================

    printer.text(
        f"DATA: {data_completa}\n"
    )

    printer.text(
        f"NF-E: {pesagem.nfe or '-'}\n"
    )

    printer.text("\n\n\n")

    # =========================================
    # FINAL
    # =========================================

    printer.cut()

    return printer.output


def imprimir_ticket(pesagem, nome_impressora="ELGIN i9(USB)"):
    """
    Gera o ticket ESC/POS e envia diretamente
    para a impressora instalada no Windows.
    """

    comandos = gerar_ticket_escpos(pesagem)

    handle = win32print.OpenPrinter(
        nome_impressora
    )

    try:

        win32print.StartDocPrinter(
            handle,
            1,
            (
                "Ticket de Pesagem",
                None,
                "RAW"
            )
        )

        win32print.StartPagePrinter(
            handle
        )

        win32print.WritePrinter(
            handle,
            comandos
        )

        win32print.EndPagePrinter(
            handle
        )

        win32print.EndDocPrinter(
            handle
        )

    finally:

        win32print.ClosePrinter(
            handle
        )

    return True