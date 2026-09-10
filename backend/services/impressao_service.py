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
    Gera os comandos ESC/POS do ticket
    para a Elgin i9.
    """

    printer = Dummy()

    # =========================================
    # INICIALIZAÇÃO
    # =========================================

    printer.hw("init")


    # =========================================
    # CABEÇALHO
    # =========================================

    printer.set(
        align="center",
        bold=True,
        width=2,
        height=2
    )

    printer.text(
        "TICKET DE PESAGEM\n"
    )

    printer.set(
        align="center",
        bold=True,
        width=1,
        height=1
    )

    printer.text(
        f"Nº {pesagem.ticket}\n"
    )

    printer.text(
        f"PLACA: {pesagem.placa}\n"
    )

    printer.text("\n")

    printer.set(
        align="left",
        bold=False
    )

    printer.text(
        "----------------------------------------\n"
    )


    # =========================================
    # CLIENTE
    # =========================================

    printer.set(
        align="left",
        bold=True
    )

    printer.text(
        "CLIENTE\n"
    )

    printer.set(
        bold=False
    )

    printer.text(
        f"{pesagem.cliente}\n"
    )

    printer.text(
        f"Transportadora: {pesagem.transportadora or '-'}\n"
    )

    printer.text(
        f"Telefone: {pesagem.telefone or '-'}\n"
    )

    printer.text("\n")


    # =========================================
    # PRODUTO
    # =========================================

    printer.set(
        bold=True
    )

    printer.text(
        "PRODUTO\n"
    )

    printer.set(
        bold=False
    )

    printer.text(
        f"Descricao: {pesagem.descricao or '-'}\n"
    )

    printer.text(
        f"Quantidade: {pesagem.quantidade or '-'}\n"
    )

    printer.text("\n")


    # =========================================
    # VALORES
    # =========================================

    printer.set(
        bold=True
    )

    printer.text(
        "VALORES\n"
    )

    printer.set(
        bold=False
    )

    printer.text(
        f"Valor produto:      R$ {pesagem.valor_produto or 0:.2f}\n"
    )

    printer.text(
        f"Total dos itens:    R$ {pesagem.total_itens or 0:.2f}\n"
    )

    printer.text(
        f"Qtd. total itens:      {pesagem.quantidade_total_itens or 0:.2f}\n"
    )

    printer.text(
        f"Valor total:        R$ {pesagem.valor_total or 0:.2f}\n"
    )

    printer.text(
        f"Desconto:           R$ {pesagem.desconto or 0:.2f}\n"
    )

    printer.text(
        f"Pagamento: {pesagem.pagamento or '-'}\n"
    )

    printer.text("\n")


    # =========================================
    # VALOR A PAGAR
    # =========================================

    printer.set(
        align="center",
        bold=True,
        width=2,
        height=2
    )

    printer.text(
        f"R$ {pesagem.valor_pagar or 0:.2f}\n"
    )

    printer.set(
        align="center",
        bold=True,
        width=1,
        height=1
    )

    printer.text(
        "VALOR A PAGAR\n"
    )

    printer.text("\n")


    # =========================================
    # PESAGEM
    # =========================================

    printer.set(
        align="left",
        bold=False
    )

    printer.text(
        "----------------------------------------\n"
    )

    printer.set(
        align="center",
        bold=True
    )

    printer.text(
        "PESAGEM\n"
    )

    printer.text("\n")


    # Tara
    printer.set(
        bold=False
    )

    printer.text(
        f"Tara:   {pesagem.tara:.3f} kg\n"
    )

    printer.text(
        f"Bruto:  {pesagem.peso_bruto:.3f} kg\n"
    )

    printer.text("\n")


    # =========================================
    # PESO LÍQUIDO - DESTAQUE
    # =========================================

    printer.set(
        align="center",
        bold=True,
        width=2,
        height=2
    )

    printer.text(
        f"{pesagem.peso_liquido:.3f} kg\n"
    )

    printer.set(
        width=1,
        height=1
    )

    printer.text(
        "PESO LIQUIDO\n"
    )

    printer.text("\n")


    # =========================================
    # DATAS
    # =========================================

    printer.set(
        align="left",
        bold=False
    )

    printer.text(
        "----------------------------------------\n"
    )

    data = pesagem.data.strftime("%d/%m/%Y")
    data_completa = pesagem.data.strftime(
        "%d/%m/%Y %H:%M"
    )

    printer.text(
        f"Data Entrada: {data}\n"
    )

    printer.text(
        f"Data Saida:   {data}\n"
    )

    printer.text("\n")


    # =========================================
    # NF-E / DATA
    # =========================================

    printer.set(
        bold=True
    )

    printer.text(
        f"DATA: {data_completa}\n"
    )

    printer.text(
        f"NF-E: {pesagem.nfe or '-'}\n"
    )

    printer.set(
        bold=False
    )

    printer.text("\n\n")


    # =========================================
    # FINAL
    # =========================================

    printer.set(
        align="center",
        bold=True
    )

    printer.text(
        "Obrigado!\n"
    )

    printer.text("\n\n\n")

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