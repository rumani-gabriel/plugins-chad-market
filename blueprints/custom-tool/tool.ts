import { tool } from "@opencode-ai/plugin"

export default tool({
  description: "QUE HACE (esto es lo que ve el modelo)",
  args: {
    ejemplo: tool.schema.string().describe("para que sirve este argumento"),
  },
  async execute(args, context) {
    // context.directory = directorio de trabajo de la sesion
    return `resultado para ${args.ejemplo}`
  },
})
