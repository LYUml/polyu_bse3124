"""Exercise the real stdio MCP transport with a separate synthetic DXF."""
import asyncio, json, os
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import ezdxf

ROOT = Path(__file__).resolve().parents[1]

async def main():
    folder = ROOT / '05_Calculations' / '00_Smoke_Test'
    folder.mkdir(parents=True, exist_ok=True)
    drawing = ezdxf.new('R2018')
    drawing.layers.new('E-TEST-LIGHT', dxfattribs={'color': 2})
    for x in (0, 1200, 2400):
        drawing.modelspace().add_circle((x, 0), 150, dxfattribs={'layer': 'E-TEST-LIGHT'})
    path = folder / 'synthetic_three_lights.dxf'
    drawing.saveas(path)
    assert len(ezdxf.readfile(path).modelspace().query('CIRCLE')) == 3
    env = dict(os.environ, AUTOCAD_MCP_BACKEND='ezdxf', ALLOWED_PATHS=str(ROOT / '05_Calculations'), ACADMCP_STATE_DIR=str(folder / 'mcp_state'))
    params = StdioServerParameters(command=str(ROOT / '.venv/Scripts/autocad-mcp.exe'), env=env, cwd=str(ROOT))
    report = {'synthetic_dxf_roundtrip': True}
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            report['advertised_tools'] = [tool.name for tool in tools.tools]
            result = await session.call_tool('system_about', {})
            report['system_about'] = result.model_dump(mode='json')
            assert not result.isError
    (ROOT / '07_Project_Notes/verification/mcp_smoke_test.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('PASS: stdio MCP initialize/list_tools/system_about; synthetic DXF contains 3 circles')

if __name__ == '__main__':
    asyncio.run(main())
