using Microsoft.AspNetCore.Mvc;
using SiT1_server.Core;
using System.Text;

namespace SiT1_server.Controllers;

[Route("api")]
[ApiController]
public class Controller : ControllerBase
{
    [HttpPost]
    public async Task<IActionResult> ParseString(Request request)
    {
        if (Encoding.Unicode.GetByteCount(request.String) > 256)
            return BadRequest("String size is more than 256 bytes");

        try
        {
            var half = request.String[..(request.Length / 2)];
            return Ok(half);
        }
        catch (ArgumentOutOfRangeException _)
        {
            return BadRequest("Passed string length in more than real one");
        }
    }

}