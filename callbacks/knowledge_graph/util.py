import copy
import os
import pickle
import shutil

import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

MAX_NUM_CHARS_DISPLAY = 10


def convert_graph_documents_to_edge_list(
    graph_documents,
    edge_list_path="D:/llm_experiments/knowledge-graph/static/edge_list.tsv",
    node_list_path="D:/llm_experiments/knowledge-graph/static/node_list.pickle",
    orphan_list_path="D:/llm_experiments/knowledge-graph/static/orphan_list.txt",
):
    edge_list = []
    node_list = {}
    for graph_document in graph_documents:
        for relationship in graph_document.relationships:
            edge_list.append(
                [relationship.source.id, relationship.target.id, relationship.type]
            )

        for node in graph_document.nodes:
            node_list[node.id] = node.type

    with open(edge_list_path, "w", encoding="utf-8") as f:
        for edge in edge_list:
            f.write(f"{edge[0]}\t{edge[1]}\t{edge[2]}\n")

    with open(
        node_list_path,
        "wb",
    ) as f:
        pickle.dump(node_list, f, protocol=pickle.HIGHEST_PROTOCOL)

    # Create empty orphan node list file
    with open(orphan_list_path, "w", encoding="utf-8") as f:
        pass

    # Create copies in order to preserve the original ones
    shutil.copyfile(edge_list_path, f"{edge_list_path}.new")
    shutil.copyfile(node_list_path, f"{node_list_path}.new")
    shutil.copyfile(orphan_list_path, f"{orphan_list_path}.new")


def parse_edit_node_queries(queries):
    for query in queries.split("\n"):
        query = query.strip().split("|")
        type = query[0].strip()

        if type.lower() == "name":
            standard_name = query[1].strip()
            alt_names = [name.strip() for name in query[2:]]
            edit_node_name(standard_name, alt_names)

        elif type.lower() == "type":
            node = query[1].strip()
            type = query[2].strip()
            edit_node_type(node, type)


def edit_node_name(
    standard_name,
    alt_names,
    edge_list_path="D:/llm_experiments/knowledge-graph/static/edge_list.tsv.new",
    node_list_path="D:/llm_experiments/knowledge-graph/static/node_list.pickle.new",
):
    with open(f"{edge_list_path}.temp", "w", encoding="utf-8") as f_new, open(
        f"{node_list_path}.temp", "wb"
    ) as g_new:
        pass

    with open(edge_list_path, "r", encoding="utf-8") as f, open(
        f"{edge_list_path}.temp", "a", encoding="utf-8"
    ) as f_new:
        for line in f:
            node1, node2, relationship = line.strip().split("\t")
            node1_write = node1
            node2_write = node2
            if node1 in alt_names:
                node1_write = standard_name
            if node2 in alt_names:
                node2_write = standard_name

            f_new.write(f"{node1_write}\t{node2_write}\t{relationship}\n")

    with open(node_list_path, "rb") as f, open(f"{node_list_path}.temp", "wb") as f_new:
        node_list = pickle.load(f)
        for name in alt_names:
            try:
                node_list.pop(name)
            except KeyError:
                pass

        pickle.dump(node_list, f_new, protocol=pickle.HIGHEST_PROTOCOL)

    # Update copies
    shutil.copyfile(f"{edge_list_path}.temp", edge_list_path)
    shutil.copyfile(f"{node_list_path}.temp", node_list_path)


def edit_node_type(
    node,
    type,
    node_list_path="D:/llm_experiments/knowledge-graph/static/node_list.pickle.new",
):
    with open(node_list_path, "rb") as f, open(f"{node_list_path}.temp", "wb") as f_new:
        node_list = pickle.load(f)
        try:
            node_list[node] = type
        except KeyError:
            pass

        pickle.dump(node_list, f_new, protocol=pickle.HIGHEST_PROTOCOL)

    # Update copies
    shutil.copyfile(f"{node_list_path}.temp", node_list_path)


def parse_add_node_queries(queries):
    for query in queries.split("\n"):
        node = query.strip()
        add_node(node)


def add_node(
    node,
    node_list_path="D:/llm_experiments/knowledge-graph/static/node_list.pickle.new",
    orphan_list_path="D:/llm_experiments/knowledge-graph/static/orphan_list.txt.new",
):
    with open(orphan_list_path, "a", encoding="utf-8") as f:
        f.write(f"{node}\n")

    with open(node_list_path, "rb") as f, open(f"{node_list_path}.temp", "wb") as f_new:
        node_list = pickle.load(f)
        node_list[node] = "Entity"

        pickle.dump(node_list, f_new, protocol=pickle.HIGHEST_PROTOCOL)

    # Update copies
    shutil.copyfile(f"{node_list_path}.temp", node_list_path)


def parse_delete_node_queries(queries):
    for query in queries.split("\n"):
        node = query.strip()
        delete_node(node)


def delete_node(
    node,
    edge_list_path="D:/llm_experiments/knowledge-graph/static/edge_list.tsv.new",
    node_list_path="D:/llm_experiments/knowledge-graph/static/node_list.pickle.new",
):
    with open(f"{edge_list_path}.temp", "w", encoding="utf-8") as f_new, open(
        f"{node_list_path}.temp", "wb"
    ) as g_new:
        pass

    with open(edge_list_path, "r", encoding="utf-8") as f, open(
        f"{edge_list_path}.temp", "a", encoding="utf-8"
    ) as f_new:
        for line in f:
            node1, node2, relationship = line.strip().split("\t")
            if node1 != node and node2 != node:
                f_new.write(f"{node1}\t{node2}\t{relationship}\n")

    with open(node_list_path, "rb") as f, open(f"{node_list_path}.temp", "wb") as f_new:
        node_list = pickle.load(f)
        try:
            node_list.pop(node)
        except KeyError:
            pass

        pickle.dump(node_list, f_new, protocol=pickle.HIGHEST_PROTOCOL)

    # Update copies
    shutil.copyfile(f"{edge_list_path}.temp", edge_list_path)
    shutil.copyfile(f"{node_list_path}.temp", node_list_path)


def parse_edit_relationship_queries(queries):
    for query in queries.split("\n"):
        query = query.strip().split("|")
        source_node = query[0].strip()
        target_node = query[1].strip()
        old_relationship = query[2].strip()
        new_relationship = query[3].strip()
        edit_relationship(source_node, target_node, old_relationship, new_relationship)


def edit_relationship(
    source_node,
    target_node,
    old_relationship,
    new_relationship,
    edge_list_path="D:/llm_experiments/knowledge-graph/static/edge_list.tsv.new",
):
    with open(f"{edge_list_path}.temp", "w", encoding="utf-8") as f_new:
        pass

    with open(edge_list_path, "r", encoding="utf-8") as f, open(
        f"{edge_list_path}.temp", "a", encoding="utf-8"
    ) as f_new:
        for line in f:
            node1, node2, relationship = line.strip().split("\t")
            relationship_write = relationship
            if (
                node1 == source_node
                and node2 == target_node
                and relationship == old_relationship
            ):
                relationship_write = new_relationship

            f_new.write(f"{node1}\t{node2}\t{relationship_write}\n")

    # Update copies
    shutil.copyfile(f"{edge_list_path}.temp", edge_list_path)


def parse_add_relationship_queries(queries):
    for query in queries.split("\n"):
        query = query.strip().split("|")
        source_node = query[0].strip()
        target_node = query[1].strip()
        relationship = query[2].strip()
        add_relationship(source_node, target_node, relationship)


def add_relationship(
    source_node,
    target_node,
    relationship,
    edge_list_path="D:/llm_experiments/knowledge-graph/static/edge_list.tsv.new",
):
    with open(edge_list_path, "a", encoding="utf-8") as f:
        f.write(f"{source_node}\t{target_node}\t{relationship}\n")


def parse_delete_relationship_queries(queries):
    for query in queries.split("\n"):
        query = query.strip().split("|")
        source_node = query[0].strip()
        target_node = query[1].strip()
        relationship = query[2].strip()
        delete_relationship(source_node, target_node, relationship)


def delete_relationship(
    source_node,
    target_node,
    relationship,
    edge_list_path="D:/llm_experiments/knowledge-graph/static/edge_list.tsv.new",
    orphan_list_path="D:/llm_experiments/knowledge-graph/static/orphan_list.txt.new",
):
    with open(f"{edge_list_path}.temp", "w", encoding="utf-8") as f_new:
        pass

    with open(edge_list_path, "r", encoding="utf-8") as f, open(
        f"{edge_list_path}.temp", "a", encoding="utf-8"
    ) as f_new:
        for line in f:
            node1, node2, rel = line.strip().split("\t")
            if node1 != source_node or node2 != target_node or relationship != rel:
                f_new.write(f"{node1}\t{node2}\t{rel}\n")

    # Check if either of the nodes is now an orphan
    is_source_node_present = False
    is_target_node_present = False
    with open(f"{edge_list_path}.temp", encoding="utf-8") as f:
        for line in f:
            node1, node2, _ = line.strip().split("\t")
            if (
                node1 == source_node
                or node1 == target_node
                or node2 == source_node
                or node2 == target_node
            ):
                is_source_node_present = True
                is_target_node_present = True

    with open(orphan_list_path, "a") as f:
        if not is_source_node_present:
            f.write(f"{source_node}\n")
        if not is_target_node_present:
            f.write(f"{target_node}\n")

    # Update copies
    shutil.copyfile(f"{edge_list_path}.temp", edge_list_path)


def get_text_color(bgcolor):
    rgb = tuple(int(bgcolor.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
    luminance = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255

    if luminance > 0.5:
        return "black"

    return "white"


def make_graph(
    initial=False,
    graph_documents_path="D:/llm_experiments/knowledge-graph/static/graph_documents.pickle",
    edge_list_path="D:/llm_experiments/knowledge-graph/static/edge_list.tsv.new",
    node_list_path="D:/llm_experiments/knowledge-graph/static/node_list.pickle.new",
    orphan_list_path="D:/llm_experiments/knowledge-graph/static/orphan_list.txt.new",
):
    if initial:
        with open(graph_documents_path, "rb") as f:
            graph_documents = pickle.load(f)

        convert_graph_documents_to_edge_list(graph_documents)

    # Read edge list
    G = nx.read_edgelist(
        edge_list_path,
        data=(("relationship", str),),
        delimiter="\t",
        create_using=nx.DiGraph,
    )

    # Read node type mapping
    with open(node_list_path, "rb") as f:
        node_list = pickle.load(f)

    # Handle orphan nodes
    with open(orphan_list_path, encoding="utf-8") as f:
        for line in f:
            orphan_node = line.strip()
            if orphan_node in G:
                continue

            G.add_node(orphan_node)

    # if not initial:
    #     from cdlib import algorithms, readwrite

    #     g = nx.convert_node_labels_to_integers(G, ordering="sorted").to_undirected()
    #     coms = algorithms.louvain(g)

    #     with open("graph.pickle", "wb") as f:
    #         pickle.dump(G, f, protocol=pickle.HIGHEST_PROTOCOL)

    #     readwrite.write_community_csv(
    #         coms,
    #         f"hello.txt",
    #         "\t",
    #     )

    node_degrees = {}
    max_degree = 0
    for node, degree in G.degree():
        if degree > max_degree:
            max_degree = degree
        node_degrees[node] = degree

    elements = copy.deepcopy(nx.cytoscape_data(G)["elements"])

    cmap = plt.get_cmap("coolwarm", len(set(node_list.values())))
    color_map = {}
    for idx, node_type in enumerate(sorted(list(set(node_list.values())))):
        color_map[node_type] = matplotlib.colors.rgb2hex(cmap(idx))

    for node in elements["nodes"]:
        if len(node["data"]["name"]) > MAX_NUM_CHARS_DISPLAY:
            node["data"]["name"] = node["data"]["name"][:MAX_NUM_CHARS_DISPLAY] + "..."
        node["data"]["degree"] = node_degrees[node["data"]["id"]]
        node["data"]["type"] = node_list[node["data"]["id"]]
        node["data"]["bgcolor"] = color_map[node["data"]["type"]]
        node["data"]["textcolor"] = get_text_color(node["data"]["bgcolor"])

    return elements, max_degree


def convert_insights_to_df(
    insights_path="D:/llm_experiments/knowledge-graph/static/insights",
    titles_path="D:/llm_experiments/knowledge-graph/static/titles",
):
    insights = []
    for insight_file in os.listdir(insights_path):
        with open(f"{insights_path}/{insight_file}", encoding="utf-8") as f:
            insight_group = []
            for line in f:
                line = line.strip()
                if not line:
                    continue

                if line.startswith("Here"):
                    continue

                if line.startswith("*"):
                    line = line[len("* ") :]

                insight_group.append(line)

            insights.append(insight_group)

    titles = []
    for title_file in os.listdir(titles_path):
        with open(f"{titles_path}/{title_file}", encoding="utf-8") as f:
            for line in f:
                titles.append(line.strip())
                break

    insights_matrix = []
    for title, insight_group in zip(titles, insights):
        for insight in insight_group:
            insights_matrix.append([title, insight])

    return pd.DataFrame(insights_matrix, columns=["Insight Group", "Insight"])


def get_relationships_with_node(
    node,
    edge_list_path="D:/llm_experiments/knowledge-graph/static/edge_list.tsv.new",
):
    relationships = []

    with open(edge_list_path, encoding="utf-8") as f:
        for line in f:
            node1, node2, relationship = line.strip().split("\t")
            if node1 == node:
                relationships.append(f"{relationship} {node2}")
            if node == node2:
                relationships.append(f"{node1} {relationship}")

    return relationships
