from pathlib import Path

from langchain_core.messages import BaseMessage, HumanMessage

from lib.langgraph.managers import BaseFileManager


async def convert_to_openai_messages(
    messages: list[BaseMessage],
    file_manager: BaseFileManager,
) -> list[BaseMessage]:
    """
    OpenAI(Chat Completions / Responses API)용 메시지 변환기.

    - image  -> image_url (base64)
    - document -> text (내용을 문자열로 풀어서 삽입)
    """

    result: list[BaseMessage] = []

    for message in messages:
        # Human + multipart content만 처리
        if message.type != "human" or not isinstance(message.content, list):
            result.append(message)
            continue

        blocks: list[dict] = []

        for block in message.content:
            block_type = block.get("type")

            # --------------------------------------------------
            # Image
            # --------------------------------------------------
            if block_type == "image":
                file = await file_manager.read(block["filename"])

                blocks.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{file.mime_type};base64,{file.to_base64()}"},
                    }
                )
                blocks.append(
                    {
                        "type": "text",
                        "text": f"{file.filename} uploaded.",
                    }
                )

            # --------------------------------------------------
            # Document
            # --------------------------------------------------
            elif block_type == "document":
                file = await file_manager.read(block["filename"])
            #                 ext = Path(file.filename).suffix.lower()

            #                 text = _document_to_text(file.raw, ext)

            #                 blocks.append(
            #                     {
            #                         "type": "text",
            #                         "text": f"""The file "{file.filename}" has been uploaded.

            # {text}
            # """,
            #     }
            # )

            # --------------------------------------------------
            # Plain text or already OpenAI-compatible block
            # --------------------------------------------------
            else:
                blocks.append(block)

        result.append(HumanMessage(blocks))

    return result
