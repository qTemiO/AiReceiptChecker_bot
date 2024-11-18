def form_pdf_metadata_reply(z_check: bool, producer_check: bool, meta_check: bool) -> str:
    text = "Результаты прохождения проверок метаданных: \n"

    text += "\nПроверка нестандартной временной зоны: "
    text += "✔️" if z_check else "🛑"

    text += "\nПроверка поставщика ПО pdf-документов: "
    text += "✔️" if producer_check else "🛑"

    text += "\nПроверка кодировки в метаданных: "
    text += "✔️" if meta_check else "🛑"

    return text


def form_pdf_signature_reply(bert_check: bool) -> str:
    text = "Результаты прохождения проверок сигнатуры: \n"

    text += "\nПроверка BERT: "
    text += "✔️" if bert_check else "🛑"

    return text