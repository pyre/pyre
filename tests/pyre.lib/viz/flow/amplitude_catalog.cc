// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// a mock of what an interactive editor needs from the c++ layer: a catalog of the node types that
// were compiled in, each with a description and a way to make one, so that a recipe written as
// plain data, with no shapes and no c++ types in it, can be realized into a graph for any tile
// shape through the generic protocol bindings alone; the recipe is the amplitude pipeline, and its
// image must match the one the hand built pipeline encodes, byte for byte


// portability
#include <portinfo>
// STL
#include <algorithm>
#include <cassert>
#include <complex>
#include <functional>
#include <map>
#include <memory>
#include <string>
#include <utility>
#include <variant>
#include <vector>
// support
#include <pyre/journal.h>
#include <pyre/viz.h>


// type aliases
// all tiles are two dimensional
using packing_t = pyre::grid::canonical_t<2>;
using shape_t = packing_t::shape_type;
// a tile over cells of a given type
template <typename cellT>
using tile_t =
    pyre::flow::products::tile_t<pyre::grid::grid_t<packing_t, pyre::memory::heap_t<cellT>>>;
// the tiles this pipeline needs
using complex64_t = tile_t<std::complex<float>>;
using float64_t = tile_t<double>;
using float32_t = tile_t<float>;
// the encoded image
using image_t = pyre::viz::products::images::bmp_t;
// the factories this pipeline needs
using selector_t = pyre::flow::factories::selectors::amplitude_t<complex64_t, float64_t>;
using normalizer_t = pyre::flow::factories::filters::parametric_t<float64_t, float32_t>;
using colormap_t = pyre::viz::factories::colormaps::gray_t<float32_t>;
using codec_t = pyre::viz::factories::codecs::bmp_t<float32_t>;
// the protocols, which is all a catalog hands out
using node_t = pyre::flow::protocols::Node;
using product_t = pyre::flow::protocols::Product;
using factory_t = pyre::flow::protocols::Factory;
using node_ref_t = std::shared_ptr<node_t>;
using product_ref_t = std::shared_ptr<product_t>;
using factory_ref_t = std::shared_ptr<factory_t>;
// an interval
using interval_t = pyre::flow::interval_t;
// the value of a setting, whatever its type
using setting_t = std::variant<double, interval_t>;


// the catalog
// the signature of the function that makes a product with a given name and shape
using product_maker_t = auto(const std::string &, shape_t) -> product_ref_t;
// the signature of the function that makes a factory with a given name
using factory_maker_t = auto(const std::string &) -> factory_ref_t;
// the signature of the function that changes a setting of a factory by name; false if the name
// or the type of the value is not one of the factory's
using setter_t = auto(const factory_ref_t &, const std::string &, const setting_t &) -> bool;

// the direction of a slot
enum class direction_t { input, output };

// the description of a slot: its name, its direction, and the catalog key of the products it takes
struct slot_t {
    std::string name;
    direction_t direction;
    std::string product;
};

// what the catalog knows about a kind of product: how to make one of a given shape
struct product_entry_t {
    std::function<product_maker_t> make;
};

// what the catalog knows about a kind of factory
struct factory_entry_t {
    // its slots, which a palette can draw before any factory of this kind exists
    std::vector<slot_t> slots;
    // the names of its settings, which an inspector can list
    std::vector<std::string> settings;
    // how to make one
    std::function<factory_maker_t> make;
    // how to change one of its settings, by name; false if the name or the value is not one of mine
    std::function<setter_t> set;
};

// the catalog: the kinds of nodes that were compiled in, by key
struct catalog_t {
    std::map<std::string, product_entry_t> products;
    std::map<std::string, factory_entry_t> factories;
};


// register a kind of tile under {key}
template <typename tileT>
auto
registerTile(catalog_t & catalog, const std::string & key) -> void
{
    // a tile of the requested shape, every cell set to the zero of its type
    catalog.products[key] = { [](const std::string & name, shape_t shape) -> product_ref_t {
        // make it
        return tileT::create(name, shape, typename tileT::cell_type {});
    } };
    // all done
    return;
}


// build the catalog this pipeline draws from; a real one would be filled by the explicit
// instantiation lists of the library, and the slots would come from the factories themselves
auto
makeCatalog() -> catalog_t
{
    // the catalog
    catalog_t catalog;

    // the products: tiles over the cells this pipeline uses
    registerTile<complex64_t>(catalog, "tile.complex64");
    registerTile<float64_t>(catalog, "tile.float64");
    registerTile<float32_t>(catalog, "tile.float32");
    // and the encoded image
    catalog.products["image.bmp"] = { [](const std::string & name, shape_t shape) -> product_ref_t {
        // make it
        return image_t::create(name, shape);
    } };

    // the amplitude of complex cells
    catalog.factories["amplitude(complex64 -> float64)"] = {
        // the slots
        { { "signal", direction_t::input, "tile.complex64" },
          { "amplitude", direction_t::output, "tile.float64" } },
        // no settings
        {},
        // how to make one
        [](const std::string & name) -> factory_ref_t { return selector_t::create(name); },
        // how to change a setting: there are none
        [](const factory_ref_t &, const std::string &, const setting_t &) { return false; },
    };
    // the map of an interval of values onto [0,1]
    catalog.factories["parametric(float64 -> float32)"] = {
        // the slots
        { { "signal", direction_t::input, "tile.float64" },
          { "normalized", direction_t::output, "tile.float32" } },
        // the settings
        { "interval" },
        // how to make one
        [](const std::string & name) -> factory_ref_t { return normalizer_t::create(name); },
        // how to change a setting
        [](const factory_ref_t & factory, const std::string & name, const setting_t & value) {
            // the interval is the only one
            if (name != "interval" || !std::holds_alternative<interval_t>(value)) {
                // and nothing else is mine
                return false;
            }
            // reach the concrete factory, which owns the setting, and set it
            std::dynamic_pointer_cast<normalizer_t>(factory)->interval(std::get<interval_t>(value));
            // all done
            return true;
        },
    };
    // the gray colormap
    catalog.factories["gray(float32)"] = {
        // the slots
        { { "data", direction_t::input, "tile.float32" },
          { "red", direction_t::output, "tile.float32" },
          { "green", direction_t::output, "tile.float32" },
          { "blue", direction_t::output, "tile.float32" } },
        // no settings
        {},
        // how to make one
        [](const std::string & name) -> factory_ref_t { return colormap_t::create(name); },
        // how to change a setting: there are none
        [](const factory_ref_t &, const std::string &, const setting_t &) { return false; },
    };
    // the bitmap encoder
    catalog.factories["bmp(float32)"] = {
        // the slots
        { { "red", direction_t::input, "tile.float32" },
          { "green", direction_t::input, "tile.float32" },
          { "blue", direction_t::input, "tile.float32" },
          { "image", direction_t::output, "image.bmp" } },
        // no settings
        {},
        // how to make one
        [](const std::string & name) -> factory_ref_t { return codec_t::create(name); },
        // how to change a setting: there are none
        [](const factory_ref_t &, const std::string &, const setting_t &) { return false; },
    };

    // hand it off
    return catalog;
}


// the recipe: what an editor builds, as plain data, with no shapes and no c++ types
// a node: its id on the canvas, the catalog key of its kind, and its settings
struct recipe_node_t {
    std::string id;
    std::string kind;
    std::vector<std::pair<std::string, setting_t>> settings;
};

// a binding: a slot of a factory, and the product bound to it
struct recipe_binding_t {
    std::string factory;
    std::string slot;
    std::string product;
};

// a whole recipe
struct recipe_t {
    std::vector<recipe_node_t> nodes;
    std::vector<recipe_binding_t> bindings;
};


// the amplitude pipeline, as an editor would save it
auto
amplitudeRecipe() -> recipe_t
{
    // the nodes, products first, then factories, as a canvas lists them
    std::vector<recipe_node_t> nodes {
        { "signal", "tile.complex64", {} },
        { "magnitude", "tile.float64", {} },
        { "normalized", "tile.float32", {} },
        { "red", "tile.float32", {} },
        { "green", "tile.float32", {} },
        { "blue", "tile.float32", {} },
        { "image", "image.bmp", {} },
        { "amplitude", "amplitude(complex64 -> float64)", {} },
        { "normalizer",
          "parametric(float64 -> float32)",
          { { "interval", interval_t { 0, 10 } } } },
        { "gray", "gray(float32)", {} },
        { "bmp", "bmp(float32)", {} },
    };
    // the bindings
    std::vector<recipe_binding_t> bindings {
        { "amplitude", "signal", "signal" },
        { "amplitude", "amplitude", "magnitude" },
        { "normalizer", "signal", "magnitude" },
        { "normalizer", "normalized", "normalized" },
        { "gray", "data", "normalized" },
        { "gray", "red", "red" },
        { "gray", "green", "green" },
        { "gray", "blue", "blue" },
        { "bmp", "red", "red" },
        { "bmp", "green", "green" },
        { "bmp", "blue", "blue" },
        { "bmp", "image", "image" },
    };
    // hand it off
    return { nodes, bindings };
}


// a recipe realized for one tile shape: its nodes by id, and the catalog key of each one
struct graph_t {
    std::map<std::string, node_ref_t> nodes;
    std::map<std::string, std::string> kinds;
};


// bind the {slot} of the factory {factoryId} to the product {productId}, after checking the
// binding against the catalog; false, and nothing bound, if the catalog does not allow it
auto
bind(
    const catalog_t & catalog, graph_t & graph, const std::string & factoryId,
    const std::string & slotName, const std::string & productId) -> bool
{
    // look up the factory and the description of its kind
    auto factory = std::dynamic_pointer_cast<factory_t>(graph.nodes.at(factoryId));
    const auto & entry = catalog.factories.at(graph.kinds.at(factoryId));
    // look up the product and its kind
    auto product = std::dynamic_pointer_cast<product_t>(graph.nodes.at(productId));
    const auto & kind = graph.kinds.at(productId);
    // go through the slots of the factory
    for (const auto & slot : entry.slots) {
        // until the one named in the binding
        if (slot.name != slotName) {
            // skip the others
            continue;
        }
        // the product must be of the kind the slot takes
        if (slot.product != kind) {
            // and nothing else is bound
            return false;
        }
        // an input
        if (slot.direction == direction_t::input) {
            // is bound
            factory->addInput(slotName, product);
            // and, since what the factory computes depends on its inputs, makes it stale
            factory->flush();
            // all done
            return true;
        }
        // an output is bound, which makes it stale
        factory->addOutput(slotName, product);
        // all done
        return true;
    }
    // a slot the factory does not have
    return false;
}


// realize {recipe} into a graph of tiles of the given {shape}
auto
realize(const catalog_t & catalog, const recipe_t & recipe, shape_t shape) -> graph_t
{
    // the graph
    graph_t graph;
    // make the nodes
    for (const auto & node : recipe.nodes) {
        // remember the kind of each one
        graph.kinds[node.id] = node.kind;
        // a product
        if (catalog.products.count(node.kind)) {
            // is made at the shape of the realization
            graph.nodes[node.id] = catalog.products.at(node.kind).make(node.id, shape);
            // and has no settings
            continue;
        }
        // a factory is made
        const auto & entry = catalog.factories.at(node.kind);
        auto factory = entry.make(node.id);
        // its settings applied
        for (const auto & [name, value] : node.settings) {
            // one at a time
            [[maybe_unused]] auto applied = entry.set(factory, name, value);
            // each of which must be one of its own
            assert(applied);
        }
        // and it is filed
        graph.nodes[node.id] = factory;
    }
    // bind the slots
    for (const auto & binding : recipe.bindings) {
        // one at a time
        [[maybe_unused]] auto bound =
            bind(catalog, graph, binding.factory, binding.slot, binding.product);
        // each of which must be allowed
        assert(bound);
    }
    // hand it off
    return graph;
}


// take a realized graph apart, so its nodes can be released
auto
dismantle(const recipe_t & recipe, graph_t & graph) -> void
{
    // go through the bindings
    for (const auto & binding : recipe.bindings) {
        // find the factory
        auto factory = std::dynamic_pointer_cast<factory_t>(graph.nodes.at(binding.factory));
        // and unbind the slot, whichever side of the factory it is on
        if (factory->inputs().count(binding.slot)) {
            // an input
            factory->removeInput(binding.slot);
        } else if (factory->outputs().count(binding.slot)) {
            // or an output
            factory->removeOutput(binding.slot);
        }
    }
    // let go of the nodes
    graph.nodes.clear();
    // all done
    return;
}


// fill a signal with magnitudes 0, 1, 2, ... at phases that vary with the cell
auto
fill(complex64_t & signal) -> void
{
    // the cells
    auto & cells = signal.write();
    // go through them
    for (decltype(cells.packing().cells()) cell = 0; cell < cells.packing().cells(); ++cell) {
        // one at a time
        cells[cell] = std::polar(static_cast<float>(cell % 50), 0.1f * cell);
    }
    // and say so
    signal.flush();
    // all done
    return;
}


// the image the hand built pipeline encodes, for comparison
auto
handBuilt(shape_t shape) -> std::vector<char>
{
    // the products
    auto signal = complex64_t::create("signal", shape, {});
    auto magnitude = float64_t::create("magnitude", shape, 0.0);
    auto normalized = float32_t::create("normalized", shape, 0.0f);
    auto red = float32_t::create("red", shape, 0.0f);
    auto green = float32_t::create("green", shape, 0.0f);
    auto blue = float32_t::create("blue", shape, 0.0f);
    auto image = image_t::create("image", shape);
    // the factories
    auto selector = selector_t::create("amplitude");
    auto normalizer = normalizer_t::create("normalizer", { 0, 10 });
    auto colormap = colormap_t::create("gray");
    auto codec = codec_t::create("bmp");
    // the wiring
    selector->signal(signal);
    selector->amplitude(magnitude);
    normalizer->signal(magnitude);
    normalizer->normalized(normalized);
    colormap->data(normalized);
    colormap->red(red);
    colormap->green(green);
    colormap->blue(blue);
    codec->red(red);
    codec->green(green);
    codec->blue(blue);
    codec->image(image);
    // the data
    fill(*signal);
    // the image
    auto bytes = image->read();
    // copied out
    auto copy = std::vector<char>(
        reinterpret_cast<const char *>(bytes.data()),
        reinterpret_cast<const char *>(bytes.data()) + bytes.cells());
    // take the graph apart
    codec->removeInput("red");
    codec->removeInput("green");
    codec->removeInput("blue");
    codec->removeOutput("image");
    colormap->removeInput("data");
    colormap->removeOutput("red");
    colormap->removeOutput("green");
    colormap->removeOutput("blue");
    normalizer->removeInput("signal");
    normalizer->removeOutput("normalized");
    selector->removeInput("signal");
    selector->removeOutput("amplitude");
    // and hand off the bytes
    return copy;
}


// driver
int
main(int argc, char * argv[])
{
    // the catalog
    auto catalog = makeCatalog();
    // the recipe
    auto recipe = amplitudeRecipe();

    // a palette reads a factory's slots from the catalog, before any factory of its kind exists
    const auto & parametric = catalog.factories.at("parametric(float64 -> float32)");
    // two slots, an input and an output
    assert(parametric.slots.size() == 2);
    assert(parametric.slots[0].direction == direction_t::input);
    // and one setting
    assert(parametric.settings == std::vector<std::string> { "interval" });

    // realize the recipe for two shapes, each of which gets a graph of its own
    for (auto shape : { shape_t { 8, 8 }, shape_t { 5, 13 } }) {
        // the record of the nodes, to check that they go away
        std::vector<std::weak_ptr<node_t>> nodes;
        // the realization lives in its own scope
        {
            // build the graph
            auto graph = realize(catalog, recipe, shape);
            // remember its nodes
            for (const auto & [id, node] : graph.nodes) {
                // one at a time
                nodes.push_back(node);
            }

            // the source is filled by hand here; a real recipe would read it through a factory
            fill(*std::dynamic_pointer_cast<complex64_t>(graph.nodes.at("signal")));
            // pull the image
            auto bytes = std::dynamic_pointer_cast<image_t>(graph.nodes.at("image"))->read();
            // which must match the one the hand built pipeline encodes
            auto expected = handBuilt(shape);
            assert(bytes.cells() == expected.size());
            assert(
                std::equal(
                    expected.begin(), expected.end(),
                    reinterpret_cast<const char *>(bytes.data())));

            // a setting changed through the catalog, by name, the way an inspector would
            const auto & entry = catalog.factories.at(graph.kinds.at("normalizer"));
            auto normalizer = std::dynamic_pointer_cast<factory_t>(graph.nodes.at("normalizer"));
            // a new interval
            [[maybe_unused]] auto applied = entry.set(normalizer, "interval", interval_t { 0, 20 });
            // is accepted
            assert(applied);
            // and makes the colors stale
            assert(std::dynamic_pointer_cast<product_t>(graph.nodes.at("red"))->stale());
            // while a setting the factory does not have
            [[maybe_unused]] auto refused = entry.set(normalizer, "level", 3.0);
            // is refused
            assert(!refused);

            // a binding the catalog does not allow: the complex signal where the magnitudes go
            [[maybe_unused]] auto bound = bind(catalog, graph, "normalizer", "signal", "signal");
            // is refused
            assert(!bound);
            // and leaves the binding that was there
            auto magnitude = std::dynamic_pointer_cast<product_t>(graph.nodes.at("magnitude"));
            assert(std::dynamic_pointer_cast<factory_t>(normalizer)->input("signal") == magnitude);

            // take the graph apart
            dismantle(recipe, graph);
        }
        // and nothing outlives it
        for (const auto & node : nodes) {
            // every one of them is gone
            assert(node.expired());
        }
    }

    // all done
    return 0;
}


// end of file
