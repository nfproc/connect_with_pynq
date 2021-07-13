// blink LED circuit for PYNQ 2021.07.12 Naoki F., AIT
// ライセンスについては LICENSE.txt を参照してください．

module blink_pynq (
    input  wire        CLK, RESETN,
    input  wire [31:0] CDIV,
    output reg   [3:0] LED);

    reg [31:0] count, n_count;
    reg  [3:0] n_led;

    always @ (CDIV, count, LED) begin
        if (count >= CDIV) begin
            n_count = 1;
            n_led   = ~ LED;
        end else begin
            n_count = count + 1'b1;
            n_led   = LED;
        end
    end

    always @ (posedge CLK) begin
        if (~ RESETN) begin
            count <= 0;
            LED   <= 4'b1001;
        end else begin
            count <= n_count;
            LED   <= n_led;
        end
    end
endmodule