// knight rider circuit for PYNQ 2021.04.06 Naoki F., AIT
// ライセンスについては LICENSE.txt を参照してください．

module knight_pynq (
    input  wire        CLK, RESETN,
    input  wire [31:0] CDIV,
    output reg   [3:0] LED);

    reg [31:0] count, n_count;
    reg  [2:0] pos, n_pos;
    
    always @ (pos) begin
        case (pos)
            3'd0: LED = 4'b0001;
            3'd1: LED = 4'b0010;
            3'd2: LED = 4'b0100;
            3'd3: LED = 4'b1000;
            3'd4: LED = 4'b0100;
            3'd5: LED = 4'b0010;
            default: LED = 4'b0000;
        endcase
    end

    always @ (CDIV, count, pos) begin
        if (count >= CDIV) begin
            n_count = 1;
            if (pos == 3'd5) begin
                n_pos   = 3'd0;
            end else begin
                n_pos   = pos + 1'b1;
            end
        end else begin
            n_count = count + 1'b1;
            n_pos   = pos;
        end
    end

    always @ (posedge CLK) begin
        if (~ RESETN) begin
            count <= 0;
            pos   <= 3'd0;
        end else begin
            count <= n_count;
            pos   <= n_pos;
        end
    end
endmodule