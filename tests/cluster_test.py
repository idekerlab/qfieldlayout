from qfieldlayout import qtests

nice_cx, edge_array = qtests.get_network("qfield_test_146_359.cx", subdir="bioplex_test_networks")

qtests.cluster_nice_cx(nice_cx)

nice_cx.set_name(nice_cx.get_name() + "_clustered")

upload_message = nice_cx.upload_to("www.ndexbio.org", "dexterpratt", "cytoscaperules")
print(upload_message.replace("/v2/network", "/viewer/networks"))
