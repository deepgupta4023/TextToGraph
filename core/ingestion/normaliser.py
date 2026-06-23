from rapidfuzz import fuzz


def normalise_entities(entities, threshold=90):

    unique = []

    for entity in entities:

        name = entity["name"]

        exists = False

        for u in unique:

            score = fuzz.ratio(name.lower(), u["name"].lower())

            if score > threshold:
                exists = True
                break

        if not exists:
            unique.append(entity)

    return unique