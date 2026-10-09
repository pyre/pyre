// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// what an interactive editor needs from the c++ layer: a catalog of the kinds of nodes that were
// compiled in, filed under the spellings of their types, so that a recipe written as plain data,
// with no shapes and no c++ types in it, can be realized into a graph for any tile shape through
// the protocols alone; the recipe is the amplitude pipeline, and its image must match the one the
// hand built pipeline encodes, byte for byte


// portability
#include <portinfo>
// STL
#include <algorithm>
#include <cassert>
#include <complex>
#include <map>
#include <memory>
#include <string>
#include <utility>
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
using node_t = pyre::flow::node_t;
using product_t = pyre::flow::product_t;
using factory_t = pyre::flow::factory_t;
using node_ref_t = pyre::flow::node_ref_t;
// the catalog
using catalog_t = pyre::flow::catalog::catalog_t;
// an interval
using interval_t = pyre::flow::interval_t;
// the value of a setting, whatever its type
using setting_t = pyre::flow::setting_t;


// build the catalog this pipeline draws from
auto
makeCatalog() -> catalog_t
{
    // the catalog
    auto catalog = catalog_t();
    // the products: tiles over the cells this pipeline uses
    catalog.registerProduct<complex64_t>();
    catalog.registerProduct<float64_t>();
    catalog.registerProduct<float32_t>();
    // and the encoded image
    catalog.registerProduct<image_t>();
    // the factories
    catalog.registerFactory<selector_t>();
    catalog.registerFactory<normalizer_t>();
    catalog.registerFactory<colormap_t>();
    catalog.registerFactory<codec_t>();
    // hand it off
    return catalog;
}


// the recipe: what an editor builds, as plain data, with no shapes and no c++ types
// a node: its id on the canvas, the spelling of its type, and its settings
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
        { "signal", complex64_t::declSelf(), {} },
        { "magnitude", float64_t::declSelf(), {} },
        { "normalized", float32_t::declSelf(), {} },
        { "red", float32_t::declSelf(), {} },
        { "green", float32_t::declSelf(), {} },
        { "blue", float32_t::declSelf(), {} },
        { "image", image_t::declSelf(), {} },
        { "amplitude", selector_t::declSelf(), {} },
        { "normalizer", normalizer_t::declSelf(), { { "interval", interval_t { 0, 10 } } } },
        { "gray", colormap_t::declSelf(), {} },
        { "bmp", codec_t::declSelf(), {} },
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


// a recipe realized for one tile shape: its nodes by id
using graph_t = std::map<std::string, node_ref_t>;


// realize {recipe} into a graph of tiles of the given {shape}
auto
realize(const catalog_t & catalog, const recipe_t & recipe, shape_t shape) -> graph_t
{
    // the graph
    graph_t graph;
    // make the nodes
    for (const auto & node : recipe.nodes) {
        // a product
        if (catalog.product(node.kind)) {
            // is made at the shape of the realization
            graph[node.id] = catalog.makeProduct(node.kind, node.id, shape);
            // and has no settings
            continue;
        }
        // a factory is made
        auto factory = catalog.makeFactory(node.kind, node.id);
        // of a kind the catalog knows
        assert(factory);
        // its settings applied
        for (const auto & [name, value] : node.settings) {
            // one at a time
            [[maybe_unused]] auto applied = factory->set(name, value);
            // each of which must be one of its own
            assert(applied);
        }
        // and it is filed
        graph[node.id] = factory;
    }
    // bind the slots
    for (const auto & binding : recipe.bindings) {
        // find the factory
        auto factory = std::dynamic_pointer_cast<factory_t>(graph.at(binding.factory));
        // and the product
        auto product = std::dynamic_pointer_cast<product_t>(graph.at(binding.product));
        // bind them, which the factory checks against its slots
        [[maybe_unused]] auto bound = factory->bind(binding.slot, product);
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
        auto factory = std::dynamic_pointer_cast<factory_t>(graph.at(binding.factory));
        // and unbind the slot, whichever side of the factory it is on
        factory->unbind(binding.slot);
    }
    // let go of the nodes
    graph.clear();
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
    const auto & parametric = *catalog.factory(normalizer_t::declSelf());
    // two slots, an input and an output
    assert(parametric.slots().size() == 2);
    assert(parametric.slots()[0].reads());
    // and one setting
    assert(parametric.settings().size() == 1);
    assert(parametric.settings()[0].name() == "interval");

    // realize the recipe for two shapes, each of which gets a graph of its own
    for (auto shape : { shape_t { 8, 8 }, shape_t { 5, 13 } }) {
        // the record of the nodes, to check that they go away
        std::vector<std::weak_ptr<node_t>> nodes;
        // the realization lives in its own scope
        {
            // build the graph
            auto graph = realize(catalog, recipe, shape);
            // remember its nodes
            for (const auto & [id, node] : graph) {
                // one at a time
                nodes.push_back(node);
            }

            // the source is filled by hand here; a real recipe would read it through a factory
            fill(*std::dynamic_pointer_cast<complex64_t>(graph.at("signal")));
            // pull the image
            auto bytes = std::dynamic_pointer_cast<image_t>(graph.at("image"))->read();
            // which must match the one the hand built pipeline encodes
            auto expected = handBuilt(shape);
            assert(bytes.cells() == expected.size());
            assert(
                std::equal(
                    expected.begin(), expected.end(),
                    reinterpret_cast<const char *>(bytes.data())));

            // a setting changed by name, the way an inspector would
            auto normalizer = std::dynamic_pointer_cast<factory_t>(graph.at("normalizer"));
            // a new interval
            [[maybe_unused]] auto applied = normalizer->set("interval", interval_t { 0, 20 });
            // is accepted
            assert(applied);
            // and makes the colors stale
            assert(std::dynamic_pointer_cast<product_t>(graph.at("red"))->stale());
            // while a setting the factory does not have
            [[maybe_unused]] auto refused = normalizer->set("level", 3.0);
            // is refused
            assert(!refused);

            // a binding the factory does not allow: the complex signal where the magnitudes go
            auto signal = std::dynamic_pointer_cast<product_t>(graph.at("signal"));
            [[maybe_unused]] auto bound = normalizer->bind("signal", signal);
            // is refused
            assert(!bound);
            // and leaves the binding that was there
            auto magnitude = std::dynamic_pointer_cast<product_t>(graph.at("magnitude"));
            assert(normalizer->input("signal") == magnitude);

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
