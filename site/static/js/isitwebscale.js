import Dlite from "//unpkg.com/dlite@0.17.0";

Dlite({
  el: "#app",
  data: {
    emptySpaces: ["Black holes aren't", "The void isn't"],
    db: {},
    dbKeys: [],
    searchTerm: "",
    result: "",
    resultStyle: {},
    spinnerStyle: {},
    examples: "",
  },
  created() {
    this.loadDb();

    addEventListener("hashchange", () => {
      this.updateSearchFromHash();
      this.refreshExamples();
    });
  },
  loadDb() {
    fetch("/isitwebscale.json")
      .then((response) => response.json())
      .then((_) => {
        this.data.db = _;
        this.data.dbKeys = Object.keys(this.data.db);

        this.refreshExamples();
        this.updateSearchFromHash();
      });
  },
  getRandom(array) {
    return array[Math.floor(Math.random() * array.length)];
  },
  refreshExamples() {
    var randomExamples = new Set();
    this.getSearchTermFromHash();

    while (this.data.dbKeys.length > 0 && randomExamples.size < 3) {
      let key = this.getRandom(this.data.dbKeys);

      if (key === this.data.searchTerm) {
        continue;
      }

      randomExamples.add(key);
    }

    if (randomExamples) {
      this.data.examples = "Some examples: ";

      randomExamples.forEach((key) => {
        this.data.examples += `<a href="#${key}">${key}</a>, `;
      });

      this.data.examples = this.data.examples.slice(0, -2);
      this.data.examples +=
        ". Add your own by <a href='https://github.com/adamghill/isitwebscale'>forking the repo</a>.";
    }
  },
  getSearchTermFromHash() {
    if (location.hash) {
      let searchTerm = location.hash.slice(1);
      this.data.searchTerm = searchTerm.replace("%20", " ");
    } else {
      this.data.searchTerm = "";
    }
  },
  updateSearchFromHash() {
    this.getSearchTermFromHash();

    if (this.data.searchTerm) {
      const el = this.el.querySelector("#search");
      el.value = this.data.searchTerm;
      this.search();
    }
  },
  startSpinner() {
    this.data.spinnerStyle["display"] = "inline-block";

    setTimeout(() => {
      this.data.spinnerStyle["display"] = "none";
    }, 500);
  },
  search() {
    const el = this.el.querySelector("#search");
    this.data.searchTerm = el.value.toLowerCase();

    this.startSpinner();

    this.data.result = "";
    this.data.resultStyle["color"] = "#666";

    if (this.data.searchTerm.trim()) {
      for (let key in this.data.db) {
        if (this.data.searchTerm === key) {
          this.data.result = this.data.db[key];
          this.data.resultStyle["color"] = "var(--success-color)";

          history.pushState({}, "", `#${this.data.searchTerm}`);

          break;
        }
      }

      if (!this.data.result) {
        this.data.result = `<em>${this.data.searchTerm}</em> can't be web scale because I've never even heard of it.`;
      }
    } else {
      let emptySpace = this.getRandom(this.data.emptySpaces);
      this.data.result = `${emptySpace} web scale and neither is an empty string.`;
    }
  },
});
