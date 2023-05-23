Langchain: Register Custom Callbacks
=====================================

Lanarky auto-detects the required callback handler based on input chain type using a callback registry.
While the default registry is sufficient for most use cases, you can register your own callbacks for custom chain types.

We will use a small example to understand how to register custom callbacks:

Let's first create a custom chain called ``ConversationalRetrievalWithSourcesChain``:

.. code-block:: python

    import re
    from typing import Any, Dict, List, Optional
    from langchain.chains import ConversationalRetrievalChain
    from langchain.callbacks.manager import (
        AsyncCallbackManagerForChainRun,
        CallbackManagerForChainRun,
    )

    class ConversationalRetrievalWithSourcesChain(ConversationalRetrievalChain):
        """Chain for chatting with sources over documents."""

        sources_output_key: str = "sources"  #: :meta private:

        @property
        def output_keys(self) -> List[str]:
            """Return the output keys.

            :meta private:
            """
            _output_keys = [self.output_key]
            _output_keys.append(self.sources_output_key)
            if self.return_source_documents:
                _output_keys = _output_keys + ["source_documents"]
            return _output_keys

        def _call(
            self,
            inputs: Dict[str, Any],
            run_manager: Optional[CallbackManagerForChainRun] = None,
        ) -> Dict[str, Any]:
            result = super()._call(
                inputs=inputs,
                run_manager=run_manager,
            )
            answer = result[self.output_key]
            if re.search(r"SOURCES:\s", answer):
                answer, sources = re.split(r"SOURCES:\s", answer)
            else:
                sources = ""
            result[self.output_key] = answer
            result[self.sources_output_key] = sources
            return result

        async def _acall(
            self,
            inputs: Dict[str, Any],
            run_manager: Optional[AsyncCallbackManagerForChainRun] = None,
        ) -> Dict[str, Any]:
            result = await super()._acall(
                inputs=inputs,
                run_manager=run_manager,
            )
            answer = result[self.output_key]
            if re.search(r"SOURCES:\s", answer):
                answer, sources = re.split(r"SOURCES:\s", answer)
            else:
                sources = ""
            result[self.output_key] = answer
            result[self.sources_output_key] = sources
            return result

Next, we will define a new streaming callback handler and add it to the registry:

.. code-block:: python

    from lanarky.register import register_streaming_callback

    @register_streaming_callback("ConversationalRetrievalWithSourcesChain")
    class AsyncConversationalRetrievalWithSourcesChainStreamingCallback(
        AsyncConversationalRetrievalChainStreamingCallback
    ):
        """AsyncStreamingResponseCallback handler for ConversationalRetrievalWithSourcesChain."""
        pass

Once your callback handler is registered, Lanarky will automatically detect it using your custom chain when
you use the ``StreamingResponse`` class in your FastAPI application.

For more register functions, check out the ``lanarky.register`` module
`reference <https://lanarky.readthedocs.io/en/latest/lanarky/lanarky.register.html>`_.
