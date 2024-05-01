<template>
  <header class="bg-white shadow-sm">
    <nav
      class="mx-auto flex max-w-7xl items-center justify-between p-4 lg:px-8"
      aria-label="Global"
    >
      <div class="flex lg:flex-1">
        <a href="#" class="-m-1.5 p-1.5">
          <span class="font-semibold text-xl">OLCScript</span>
        </a>
      </div>
    </nav>
  </header>
  <div class="max-w-7xl m-auto">
    <div class="p-4">
      <Menu as="div" class="relative inline-block text-left mb-2">
        <div>
          <MenuButton
            class="inline-flex w-full justify-center gap-x-1.5 bg-white px-1 pl-2 py-1.5 pb-2 text-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
          >
            Archivos
            <ChevronDownIcon
              class="-mr-1 h-5 w-5 text-gray-400"
              aria-hidden="true"
            />
          </MenuButton>
        </div>

        <transition
          enter-active-class="transition ease-out duration-100"
          enter-from-class="transform opacity-0 scale-95"
          enter-to-class="transform opacity-100 scale-100"
          leave-active-class="transition ease-in duration-75"
          leave-from-class="transform opacity-100 scale-100"
          leave-to-class="transform opacity-0 scale-95"
        >
          <MenuItems
            class="absolute left-0 z-10 w-56 origin-top-right bg-white shadow ring-1 ring-black ring-opacity-5 focus:outline-none"
          >
            <div class="py-1">
              <MenuItem v-slot="{ active }">
                <div>
                  <label
                    for="file"
                    class="w-full text-left"
                    :class="[
                      active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                      'block px-4 py-2 text-sm',
                    ]"
                  >
                    Abrir archivo
                  </label>
                  <input type="file" id="file" @change="openFile" hidden />
                </div>
              </MenuItem>
              <MenuItem v-slot="{ active }">
                <button
                  @click="newFile"
                  class="w-full text-left"
                  :class="[
                    active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                    'block px-4 py-2 text-sm',
                  ]"
                >
                  Nuevo archivo
                </button>
              </MenuItem>
            </div>
          </MenuItems>
        </transition>
      </Menu>
      <div class="flex items-end">
        <div v-for="(tab, index) in tabs" :key="index">
          <div
            class="border-x border-t border-gray-200 min-w-[90px] cursor-pointer"
            @click="actualTab = index"
          >
            <div class="p-1 flex justify-between px-2">
              <div class="pr-2">
                <input
                  class="text-sm outline-none"
                  type="text"
                  v-model="tab.name"
                />
              </div>
              <div>
                <button
                  @click="deleteFile(index)"
                  class="text-xs text-gray-500"
                >
                  <font-awesome-icon icon="times" />
                </button>
              </div>
            </div>
            <div
              :class="{
                'border-b-2 border-blue-300': index == actualTab,
                'border-b-2 border-white': index != actualTab,
              }"
            ></div>
          </div>
        </div>
      </div>
      <div class="w-full border border-gray-200 p-4">
        <div class="w-full">
          <div class="border border-gray-200 max-h-[550px] overflow-auto">
            <div class="flex pb-4">
              <div class="flex flex-col w-8 border-r border-gray-200">
                <div
                  v-for="(item, index) in getCountLines"
                  :key="index"
                  class="text-right pr-1"
                >
                  <div class="text-gray-500 text-xs leading-5">
                    {{ index + 1 }}
                  </div>
                </div>
              </div>
              <textarea
                class="w-full focus:outline-none px-1 text-sm leading-5 overflow-hidden"
                v-model="tabs[actualTab].value"
              ></textarea>
            </div>
          </div>
          <div class="pt-2 flex justify-end">
            <button
              @click="execute"
              class="inline-flex items-center bg-blue-100 px-4 h-8 text-xs font-medium text-blue-700"
            >
              <span v-if="load">
                <font-awesome-icon icon="spinner" />
              </span>
              <span v-else>Ejecutar</span>
            </button>
          </div>
          <div class="mt-4" v-if="tabs[actualTab].errors.length > 0">
            <span class="text-sm">Errores:</span>
            <table
              class="border p-2 border-gray-200 overflow-auto text-xs w-full"
            >
              <tbody>
                <tr
                  v-for="(error, index) in tabs[actualTab].errors"
                  class="border-b border-gray-200"
                >
                  <td class="p-1">{{ error }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="flex items-end">
            <div v-for="(tab, index) in resultTabs" :key="index">
              <div
                class="border-x border-t border-gray-200 min-w-[90px] cursor-pointer"
                @click="actualResultTab = index"
              >
                <div class="p-1 flex justify-between px-2">
                  <div class="pr-2">
                    <span class="text-sm">{{ tab.name }}</span>
                  </div>
                </div>
                <div
                  :class="{
                    'border-b-2 border-blue-300': index == actualResultTab,
                    'border-b-2 border-white': index != actualResultTab,
                  }"
                ></div>
              </div>
            </div>
          </div>

          <div
            v-if="tabs[actualTab].console.length > 0 && actualResultTab == 0"
          >
            <table
              class="border p-2 border-gray-200 overflow-auto text-xs w-full"
            >
              <tbody>
                <tr
                  v-for="(log, index) in tabs[actualTab].console"
                  class="border-b border-gray-200"
                >
                  <td class="p-1">
                    <textarea
                      class="w-full outline-none"
                      rows="1"
                      :value="log"
                    ></textarea>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-if="tabs[actualTab].symbols && actualResultTab == 1">
            <div v-if="Object.keys(tabs[actualTab].symbols).length > 0">
              <table
                class="border p-2 border-gray-200 overflow-auto text-xs w-full"
              >
                <tbody>
                  <tr class="border-b border-gray-200 font-semibold">
                    <td class="p-1">Identificador</td>
                    <td class="p-1">Tipo declaracion</td>
                    <td class="p-1">Tipo</td>
                    <td class="p-1">Entorno</td>
                    <td class="p-1">Tipo de variable</td>
                  </tr>
                  <tr
                    v-for="(variable, key) in tabs[actualTab].symbols"
                    class="border-b border-gray-200"
                  >
                    <td class="p-1">{{ variable.id }}</td>
                    <td class="p-1">{{ variable.varType }}</td>
                    <td class="p-1">{{ variable.type }}</td>
                    <td class="p-1">{{ variable.environment }}</td>
                    <td class="p-1">{{ variable.typeOf }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div v-if="tabs[actualTab].gen">
            <div>
              <button
                @click="copy"
                class="bg-blue-100 px-4 h-8 text-xs font-medium text-blue-700"
              >
                Copiar
              </button>

            </div>
            <div class="p-2">
              <span class="text-sm">Codigo generado:</span>
              <textarea
                class="w-full outline-none"
                style="height: 1000px;"
                rows="1000"
                :value="tabs[actualTab].gen"
              ></textarea>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
import { ChevronDownIcon } from "@heroicons/vue/20/solid";

export default {
  components: {
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    ChevronDownIcon,
  },
  data() {
    return {
      actualTab: 0,
      actualResultTab: 0,
      resultTabs: [
        {
          name: "Consola",
        },
        {
          name: "Simbolos",
        },
        {
          name: "Risc V",
        },
      ],
      tabs: [
        {
          name: "Nuevo",
          value: "",
          errors: [],
          symbols: [],
          console: [],
          gen: "",
        },
      ],
      load: false,
    };
  },
  mounted() {
    self = this;
    document.addEventListener("keydown", (e) => {
      if (e.ctrlKey && e.key === "Enter") {
        self.execute();
      }
    });
  },
  methods: {
    async execute() {
      if (this.getActualTab.value == "") {
        return;
      }
      this.load = true;

      this.tabs[this.actualTab].errors = [];
      this.tabs[this.actualTab].symbols = [];
      this.tabs[this.actualTab].console = [];
      this.tabs[this.actualTab].gen = "";

      try {
        // content-type: application/json
        const response = await axios.post(`http://127.0.0.1:5000/interpret`, {
          params: {
            value: this.tabs[this.actualTab].value,
          },
        });
        this.tabs[this.actualTab].console = response.data.console;
        this.tabs[this.actualTab].errors = response.data.exceptions;
        this.tabs[this.actualTab].symbols = response.data.ts;
        this.tabs[this.actualTab].gen = response.data.gen;
      } catch (error) {
        console.log(error);
      } finally {
        this.load = false;
      }
    },
    newFile() {
      this.tabs.push({
        name: "Nuevo archivo" + this.tabs.length,
        value: "",
        response: "",
        errors: [],
        symbols: [],
        console: [],
        gen: "",
      });
      this.actualTab = this.tabs.length - 1;
    },
    copy() {
      navigator.clipboard.writeText(this.tabs[this.actualTab].gen);
    },
    openFile(e) {
      console.log("open file", e);
      const file = e.target.files[0];
      const reader = new FileReader();
      reader.onload = (e) => {
        this.tabs.push({
          name: file.name,
          value: e.target.result,
          errors: [],
          symbols: [],
          console: [],
          gen: "",
        });
        this.actualTab = this.tabs.length - 1;
      };
      reader.readAsText(file);
    },
    deleteFile(index) {
      console.log("delete file", index);
      this.actualTab = 0;
      if (this.tabs.length == 1) {
        this.tabs[0].value = "";
        this.tabs[0].errors = [];
        this.tabs[0].console = [];
        this.tabs[0].symbols = [];
        this.tabs[0].gen = "";
      } else {
        this.actualTab = index - 1;
        this.tabs.splice(index, 1);
      }
    },
  },
  computed: {
    getActualTab() {
      return this.tabs[this.actualTab];
    },
    getCountLines() {
      return this.tabs[this.actualTab].value.split("\n").length;
    },
  },
};
</script>
