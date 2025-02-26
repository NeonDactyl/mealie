<template>
  <div>
    <slot name="activator" v-bind="{ open }" />
    <v-dialog
      v-model="dialog"
      absolute
      :width="width"
      :content-class="top ? 'top-dialog' : undefined"
      :fullscreen="$vuetify.breakpoint.xsOnly"
    >
      <v-card height="100%">
        <v-app-bar dark dense :color="color" class="">
          <v-icon large left>
            {{ icon }}
          </v-icon>
          <v-toolbar-title class="headline"> {{ title }} </v-toolbar-title>
          <v-spacer></v-spacer>
        </v-app-bar>
        <v-progress-linear v-if="loading" class="mt-1" indeterminate color="primary"></v-progress-linear>

        <div>
          <slot v-bind="{ submitEvent }" />
        </div>

        <v-divider class="mx-2"></v-divider>

        <v-card-actions>
          <slot name="card-actions">
            <v-btn
              text
              color="grey"
              @click="
                dialog = false;
                $emit('cancel');
              "
            >
              {{ $t("general.cancel") }}
            </v-btn>
            <v-spacer></v-spacer>

            <BaseButton v-if="$listeners.delete" delete secondary @click="deleteEvent" />
            <BaseButton
              v-if="$listeners.confirm"
              :color="color"
              type="submit"
              @click="
                $emit('confirm');
                dialog = false;
              "
            >
              <template #icon>
                {{ $globals.icons.check }}
              </template>
              {{ $t("general.confirm") }}
            </BaseButton>
            <BaseButton v-if="$listeners.submit" type="submit" @click="submitEvent">
              {{ submitText }}
            </BaseButton>
          </slot>
        </v-card-actions>

        <div v-if="$slots['below-actions']" class="pb-4">
          <slot name="below-actions"> </slot>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from "@nuxtjs/composition-api";
export default defineComponent({
  name: "BaseDialog",
  props: {
    value: {
      type: Boolean,
      default: false,
    },
    color: {
      type: String,
      default: "primary",
    },
    title: {
      type: String,
      default: "Modal Title",
    },
    icon: {
      type: String,
      default: null,
    },
    width: {
      type: [Number, String],
      default: "500",
    },
    loading: {
      type: Boolean,
      default: false,
    },
    top: {
      default: null,
      type: Boolean,
    },
    submitText: {
      type: String,
      // TODO Figure out how to localize this default value
      default: () => "Create",
    },
    keepOpen: {
      default: false,
      type: Boolean,
    },
  },
  setup(props, context) {
    const dialog = computed<boolean>({
      get() {
        return props.value;
      },
      set(val) {
        context.emit("input", val);
      },
    });

    return {
      dialog,
    };
  },
  data() {
    return {
      submitted: false,
    };
  },
  computed: {
    determineClose(): boolean {
      return this.submitted && !this.loading && !this.keepOpen;
    },
  },
  watch: {
    determineClose() {
      this.submitted = false;
      this.dialog = false;
    },
    dialog(val) {
      if (val) this.submitted = false;
      if (!val) this.$emit("close");
    },
  },
  methods: {
    submitEvent() {
      this.$emit("submit");
      this.submitted = true;
    },
    deleteEvent() {
      this.$emit("delete");
      this.submitted = true;
    },
    open() {
      this.dialog = true;
      this.logDeprecatedProp("open");
    },
    close() {
      this.dialog = false;
      this.logDeprecatedProp("close");
    },
    logDeprecatedProp(val: string) {
      console.warn(
        `[BaseDialog] The method '${val}' is deprecated. Please use v-model="value" to manage state instead.`
      );
    },
  },
});
</script>

<style>
.top-dialog {
  position: fixed;
  top: 0;
}
</style>
